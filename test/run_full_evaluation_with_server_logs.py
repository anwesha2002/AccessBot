#!/usr/bin/env python3
"""
Complete Evaluation System with Server and Client Logging
This script manages both server startup and client evaluation with full logging
"""

import subprocess
import time
import sys
import os
from datetime import datetime
from pathlib import Path
import signal
import atexit

class ServerAndClientLogger:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create evidence/evaluation_results directory if it doesn't exist
        os.makedirs("evidence/evaluation_results", exist_ok=True)
        self.server_log_file = f"evidence/evaluation_results/server_logs_{self.timestamp}.log"
        self.client_log_file = f"evidence/evaluation_results/client_logs_{self.timestamp}.log"
        self.server_process = None
        
    def start_server(self):
        """Start the server with logging"""
        print("🚀 Starting IT Guardian Agent Server...")
        print(f"📝 Server logs: {self.server_log_file}")
        
        # Open log file for server output
        self.server_log = open(self.server_log_file, 'w', encoding='utf-8')
        
        # Start server process with output redirection
        self.server_process = subprocess.Popen(
            [sys.executable, 'src/it_guardian_agent.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Start a thread to continuously read and log server output
        import threading
        def log_server_output():
            for line in iter(self.server_process.stdout.readline, ''):
                if line:
                    print(f"[SERVER] {line}", end='')
                    self.server_log.write(line)
                    self.server_log.flush()
        
        self.log_thread = threading.Thread(target=log_server_output, daemon=True)
        self.log_thread.start()
        
        # Wait for server to start
        print("⏳ Waiting for server to start (15 seconds)...")
        time.sleep(15)
        
        if self.server_process.poll() is not None:
            print("❌ Server failed to start!")
            return False
        
        print("✅ Server is running!")
        return True
    
    def run_evaluation(self, batch_size=2, start=0, end=None):
        """Run the evaluation with logging"""
        print(f"\n📊 Starting Evaluation...")
        print(f"📝 Client logs: {self.client_log_file}")
        
        # Build command
        cmd = [
            sys.executable, 
            'test/run_evaluation_batch_recorded.py',
            '--batch-size', str(batch_size),
            '--start', str(start)
        ]
        
        if end is not None:
            cmd.extend(['--end', str(end)])
        
        # Run evaluation
        result = subprocess.run(cmd, capture_output=False)
        
        return result.returncode == 0
    
    def stop_server(self):
        """Stop the server gracefully"""
        if self.server_process:
            print("\n🛑 Stopping server...")
            
            # Try graceful shutdown first
            self.server_process.terminate()
            
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("⚠️ Server didn't stop gracefully, forcing...")
                self.server_process.kill()
                self.server_process.wait()
            
            if hasattr(self, 'server_log'):
                self.server_log.close()
            
            print(f"✅ Server stopped. Logs saved to: {self.server_log_file}")
    
    def cleanup(self):
        """Cleanup on exit"""
        self.stop_server()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Run complete evaluation with server and client logging")
    parser.add_argument("--batch-size", type=int, default=2, help="Batch size for evaluation")
    parser.add_argument("--start", type=int, default=0, help="Start scenario index")
    parser.add_argument("--end", type=int, default=None, help="End scenario index")
    parser.add_argument("--no-server", action="store_true", help="Don't start server (assume already running)")
    
    args = parser.parse_args()
    
    print("="*60)
    print("🎯 IT Guardian Agent - Complete Evaluation System")
    print("="*60)
    
    logger = ServerAndClientLogger()
    
    # Register cleanup
    atexit.register(logger.cleanup)
    
    try:
        # Start server if needed
        if not args.no_server:
            if not logger.start_server():
                print("❌ Failed to start server. Exiting.")
                return 1
        else:
            print("⏭️ Skipping server start (--no-server flag)")
        
        # Run evaluation
        success = logger.run_evaluation(
            batch_size=args.batch_size,
            start=args.start,
            end=args.end
        )
        
        print("\n" + "="*60)
        if success:
            print("✅ Evaluation completed successfully!")
        else:
            print("❌ Evaluation completed with errors")
        
        print("\n📁 Output Files:")
        print(f"   - Server logs: {logger.server_log_file}")
        print(f"   - Client logs: Look for evaluation_batch_recording_*.log")
        print("="*60)
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
        return 130
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        if not args.no_server:
            logger.stop_server()

if __name__ == "__main__":
    sys.exit(main())
