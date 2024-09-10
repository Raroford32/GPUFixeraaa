import os
import subprocess
import sys
import time

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode('utf-8'), error.decode('utf-8')

def check_cuda():
    output, _ = run_command("nvidia-smi")
    if "NVIDIA-SMI" not in output:
        print("CUDA is not properly installed or configured.")
        print("Please ensure CUDA and NVIDIA drivers are installed and configured correctly.")
        sys.exit(1)
    print("CUDA is properly installed and configured.")

def install_dependencies():
    print("Installing required packages...")
    packages = [
        "torch", "torchvision", "torchaudio",
        "transformers", "accelerate", "gradio",
        "colorama", "markdown", "mdtex2html",
        "sentencepiece", "GitPython"
    ]
    for package in packages:
        run_command(f"pip install {package}")
    print("Required packages installed successfully.")

def clone_repository():
    print("Cloning oobabooga/text-generation-webui repository...")
    run_command("git clone https://github.com/oobabooga/text-generation-webui.git")
    os.chdir("text-generation-webui")
    print("Repository cloned successfully.")

def configure_gpu_usage():
    print("Configuring GPU usage...")
    with open("config.json", "w") as f:
        f.write('''
{
    "gpu_memory_utilization": 0.9,
    "max_input_length": 2048,
    "max_total_tokens": 4096,
    "gpu_indices": "0,1,2,3,4,5,6,7"
}
''')
    print("GPU usage configured for all 8 A100 GPUs.")

def start_web_ui():
    print("Starting the text generation web UI...")
    command = "python server.py --listen --gpu-memory-utilization 0.9 --multi-gpu"
    process = subprocess.Popen(command, shell=True)
    print("Web UI started. Please access it at http://localhost:5000")
    return process

def main():
    check_cuda()
    install_dependencies()
    clone_repository()
    configure_gpu_usage()
    web_ui_process = start_web_ui()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the web UI...")
        web_ui_process.terminate()
        web_ui_process.wait()
        print("Web UI stopped.")

if __name__ == "__main__":
    main()
