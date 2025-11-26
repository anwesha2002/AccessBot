# --- Batch Evaluation Script with Auto-Recording ---
# Run evaluation in batches + automatically record all output

import httpx
import json
import time
import os
from typing import List, Dict, Any
from datetime import datetime
import argparse
import sys

from run_evaluation import TEST_SCENARIOS, AgentEvaluator

class TeeOutput:
    """Write to both console and file"""
    def __init__(self, *outputs):
        self.outputs = outputs
        
    def write(self, text):
        for output in self.outputs:
            output.write(text)
            output.flush()
            
    def flush(self):
        for output in self.outputs:
            output.flush()

def main():
    parser = argparse.ArgumentParser(description="Run evaluation in batches with auto-recording")
    parser.add_argument("--batch-size", type=int, default=2, help="Number of scenarios per batch (default: 2)")
    parser.add_argument("--batch-delay", type=int, default=60, help="Delay between batches in seconds (default: 60)")
    parser.add_argument("--turn-delay", type=int, default=10, help="Delay between conversation turns (default: 10)")
    parser.add_argument("--scenario-delay", type=int, default=15, help="Delay between scenarios (default: 15)")
    parser.add_argument("--start", type=int, default=0, help="Start index (0-based)")
    parser.add_argument("--end", type=int, default=None, help="End index (exclusive)")
    
    args = parser.parse_args()
    
    # Setup recording
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Create evidence/evaluation_results directory if it doesn't exist
    os.makedirs("evidence/evaluation_results", exist_ok=True)
    log_file_path = f"evidence/evaluation_results/evaluation_batch_recording_{timestamp}.log"
    log_file = open(log_file_path, 'w', encoding='utf-8')
    original_stdout = sys.stdout
    sys.stdout = TeeOutput(original_stdout, log_file)
    
    try:
        # Select scenarios to run
        end_idx = args.end if args.end is not None else len(TEST_SCENARIOS)
        scenarios_to_run = TEST_SCENARIOS[args.start:end_idx]
        
        print(f"📹 Recording to: {log_file_path}")
        print("="*60)
        print("IT Guardian Agent - Batch Evaluation with Recording")
        print("="*60)
        print(f"Running scenarios {args.start} to {end_idx-1} (Total: {len(scenarios_to_run)})")
        print(f"Batch size: {args.batch_size}")
        print(f"Batch delay: {args.batch_delay}s")
        print(f"Turn delay: {args.turn_delay}s")
        print(f"Scenario delay: {args.scenario_delay}s")
        print(f"Recording: {log_file_path}")
        print("="*60)
        
        evaluator = AgentEvaluator()
        all_results = []
        
        # Process in batches
        for batch_num in range(0, len(scenarios_to_run), args.batch_size):
            batch = scenarios_to_run[batch_num:batch_num + args.batch_size]
            batch_idx = batch_num // args.batch_size + 1
            total_batches = (len(scenarios_to_run) + args.batch_size - 1) // args.batch_size
            
            print(f"\n{'='*60}")
            print(f"📦 BATCH {batch_idx}/{total_batches}")
            print(f"{'='*60}")
            
            batch_results = []
            for i, scenario in enumerate(batch):
                result = evaluator.evaluate_scenario(scenario)
                batch_results.append(result)
                all_results.append(result)
                
                # Delay between scenarios (except last in batch)
                if i < len(batch) - 1:
                    print(f"\n⏰ [Waiting {args.scenario_delay}s between scenarios...]")
                    time.sleep(args.scenario_delay)
            
            # Delay between batches (except last batch)
            if batch_num + args.batch_size < len(scenarios_to_run):
                print(f"\n{'='*60}")
                print(f"✅ [BATCH {batch_idx} COMPLETE - Waiting {args.batch_delay}s before next batch...]")
                print(f"{'='*60}")
                time.sleep(args.batch_delay)
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 EVALUATION SUMMARY")
        print(f"{'='*60}")
        
        passed = sum(1 for r in all_results if r['status'] == 'PASS')
        failed = sum(1 for r in all_results if r['status'] == 'FAIL')
        errors = sum(1 for r in all_results if r['status'] == 'ERROR')
        
        print(f"Total: {len(all_results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Errors: {errors}")
        
        # Save results to JSON file
        json_file = f"evidence/evaluation_results/evaluation_batch_results_{args.start}_{end_idx-1}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 JSON results saved to: {json_file}")
        print(f"📝 Full transcript saved to: {log_file_path}")
        
        return all_results
        
    finally:
        # Stop recording
        sys.stdout = original_stdout
        log_file.close()
        print(f"\n✅ Recording complete! Saved to: {log_file_path}")

if __name__ == "__main__":
    try:
        results = main()
    except httpx.ConnectError:
        print("\n[ERROR] Could not connect to the agent server.")
        print("Please ensure the server is running at http://127.0.0.1:8000")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
