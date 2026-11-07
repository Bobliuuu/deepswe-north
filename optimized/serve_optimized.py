"""Optimized arm: North-Mini-Code-1.0-fp8 on 1xH100. Score is the objective, so no lossy knobs (bf16 KV).
Speed knobs only where lossless: prefix caching (agent loops re-send the whole history, ~5M input tok/trial),
async scheduling, chunked prefill 2048, larger seq cap."""
import subprocess, modal

MODEL = "CohereLabs/North-Mini-Code-1.0-fp8"
image = (modal.Image.debian_slim(python_version="3.12")
         .pip_install("vllm", "cohere-melody>=0.15", "huggingface_hub[hf_transfer]")
         .env({"VLLM_USE_FLASHINFER_SAMPLER": "0", "HF_HUB_ENABLE_HF_TRANSFER": "1", "HF_HOME": "/cache/hf"}))
cache = modal.Volume.from_name("north-baseline-cache", create_if_missing=True)
app = modal.App("north-mini-code-optimized")

@app.function(image=image, gpu="H100", volumes={"/cache": cache},
              timeout=24 * 3600, scaledown_window=1800, max_containers=1)
@modal.concurrent(max_inputs=64)
@modal.web_server(8000, startup_timeout=1800)
def serve():
    subprocess.Popen(["vllm", "serve", MODEL, "--served-model-name", "north-mini-code", "--host", "0.0.0.0",
                      "--port", "8000", "--max-model-len", "262144",
                      "--enable-prefix-caching", "--max-num-batched-tokens", "2048",
                      "--max-num-seqs", "32", "--gpu-memory-utilization", "0.93",
                      "--reasoning-parser", "cohere_command4", "--enable-auto-tool-choice",
                      "--tool-call-parser", "cohere_command4"])
