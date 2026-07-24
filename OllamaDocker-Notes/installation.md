Setup
---

1. If you do not already have docker installed:

Method 1:
```
https://www.docker.com/products/docker-desktop/
```

Method 2: Homebrew *Optional*

```
https://formulae.brew.sh/cask/docker-desktop
```
Or

```zsh
brew install --cask docker-desktop
```
---

### More info:
Install, Setup and Configure Docker:

```
https://docs.docker.com/manuals/
```
Check Your Docker Installation

```
https://www.docker.com/blog/how-to-check-docker-version/
```
---
2. Docker Compose:

Change the directory to the project, and then run:

```
docker compose up --build
```
Or to run it detached in the background.

```zsh
docker compose up -d --build
```
The `-d` flag stands for detached mode


---

After completing the steps above, this is what you should see.
![Initial Boot](../OllamaDocker-Notes/Images.png)
![Initial Boot](../OllamaDocker-Notes/Containers.png)


Once running, the Containers tab shows nutrition-ollama and nutrition-web grouped together, and you can view logs or stop/restart from there without touching the terminal again.

---

To stop everything: 

```zsh
docker compose down
```
Add `-v` only if you want to wipe the pulled model too.
You usually don't, since re-pulling takes time.

---

### References

* [Ollama](https://ollama.com/)
* [Alternative Install Guide](https://namrata23.medium.com/run-llms-locally-or-in-docker-with-ollama-ollama-webui-379029060324)




---

```
(.venv) sebastiandorata@M2 4020AIServer % docker compose up --build
[+] Building 16.2s (12/12) FINISHED                                                                                                                                                                                                                                                                    
 => [internal] load local bake definitions                                                                                                                                                                                                                                                        0.0s
 => => reading from stdin 552B                                                                                                                                                                                                                                                                    0.0s
 => [internal] load build definition from Dockerfile                                                                                                                                                                                                                                              0.0s 
 => => transferring dockerfile: 201B                                                                                                                                                                                                                                                              0.0s 
 => [internal] load metadata for docker.io/library/python:3.12-slim                                                                                                                                                                                                                               0.3s 
 => [internal] load .dockerignore                                                                                                                                                                                                                                                                 0.0s
 => => transferring context: 2B                                                                                                                                                                                                                                                                   0.0s 
 => [1/5] FROM docker.io/library/python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de                                                                                                                                                                         0.0s 
 => => resolve docker.io/library/python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de                                                                                                                                                                         0.0s 
 => [internal] load build context                                                                                                                                                                                                                                                                 0.3s 
 => => transferring context: 757.62kB                                                                                                                                                                                                                                                             0.3s
 => CACHED [2/5] WORKDIR /app                                                                                                                                                                                                                                                                     0.0s
 => [3/5] COPY requirements.txt .                                                                                                                                                                                                                                                                 0.0s 
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt                                                                                                                                                                                                                                      8.1s 
 => [5/5] COPY . .                                                                                                                                                                                                                                                                                0.6s 
 => exporting to image                                                                                                                                                                                                                                                                            6.5s 
 => => exporting layers                                                                                                                                                                                                                                                                           4.7s 
 => => exporting manifest sha256:31d9909e4e0a9922f36da0c368c7ab8a9500e43d990077ddad013564276989ef                                                                                                                                                                                                 0.0s 
 => => exporting config sha256:5f1ec0f8112844d12cb047975fb7a61c9ec5fb612860bb82092042dba5935b8e                                                                                                                                                                                                   0.0s 
 => => exporting attestation manifest sha256:234d8c3490fb16af2bc0575fdbe573675184a8e5fcc07ac1e3be0bff9d60c22c                                                                                                                                                                                     0.0s 
 => => exporting manifest list sha256:202b0d2a65e69cbb60e8b3d90c33c924090575395ba1ed34bc77ebde8ce0e93a                                                                                                                                                                                            0.0s
 => => naming to docker.io/library/4020aiserver-web:latest                                                                                                                                                                                                                                        0.0s 
 => => unpacking to docker.io/library/4020aiserver-web:latest                                                                                                                                                                                                                                     1.7s 
 => resolving provenance for metadata file                                                                                                                                                                                                                                                        0.0s
[+] up 2/2                                                                                                                                                                                                                                                                                             
 ✔ Image 4020aiserver-web  Built                                                                                                                                                                                                                                                                  16.3s
 ✔ Container nutrition-web Recreated                                                                                                                                                                                                                                                               0.7s
Attaching to ollama-pull-1, nutrition-ollama, nutrition-web
nutrition-ollama  | time=2026-07-23T23:03:14.005Z level=INFO source=routes.go:1947 msg="server config" env="map[CUDA_VISIBLE_DEVICES: GGML_VK_VISIBLE_DEVICES: GPU_DEVICE_ORDINAL: HIP_VISIBLE_DEVICES: HSA_OVERRIDE_GFX_VERSION: HTTPS_PROXY: HTTP_PROXY: LLAMA_ARG_FIT: LLAMA_ARG_FIT_TARGET: NO_PROXY: OLLAMA_CONTEXT_LENGTH:0 OLLAMA_DEBUG:INFO OLLAMA_DEBUG_LOG_REQUESTS:false OLLAMA_EDITOR: OLLAMA_FLASH_ATTENTION:false OLLAMA_GO_TEMPLATE:true OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://0.0.0.0:11434 OLLAMA_IGPU_ENABLE: OLLAMA_KEEP_ALIVE:5m0s OLLAMA_KV_CACHE_TYPE: OLLAMA_LLM_LIBRARY: OLLAMA_LOAD_TIMEOUT:5m0s OLLAMA_MAX_LOADED_MODELS:0 OLLAMA_MAX_QUEUE:512 OLLAMA_MAX_TRANSFER_STREAMS:4 OLLAMA_MODELS:/root/.ollama/models OLLAMA_NOHISTORY:false OLLAMA_NOPRUNE:false OLLAMA_NO_CLOUD:false OLLAMA_NUM_PARALLEL:1 OLLAMA_ORIGINS:[http://localhost https://localhost http://localhost:* https://localhost:* http://127.0.0.1 https://127.0.0.1 http://127.0.0.1:* https://127.0.0.1:* http://0.0.0.0 https://0.0.0.0 http://0.0.0.0:* https://0.0.0.0:* app://* file://* tauri://* vscode-webview://* vscode-file://*] OLLAMA_REMOTES:[ollama.com] OLLAMA_SCHED_SPREAD:false OLLAMA_VULKAN:true ROCR_VISIBLE_DEVICES: http_proxy: https_proxy: no_proxy:]"
nutrition-ollama  | time=2026-07-23T23:03:14.005Z level=INFO source=routes.go:1949 msg="Ollama cloud disabled: false"
nutrition-ollama  | time=2026-07-23T23:03:14.005Z level=INFO source=images.go:883 msg="total blobs: 0"
nutrition-ollama  | time=2026-07-23T23:03:14.006Z level=INFO source=images.go:890 msg="total unused blobs removed: 0"
nutrition-ollama  | time=2026-07-23T23:03:14.006Z level=INFO source=routes.go:2004 msg="Listening on [::]:11434 (version 0.32.1)"
nutrition-ollama  | time=2026-07-23T23:03:14.006Z level=INFO source=runner.go:60 msg="discovering available GPUs..."
nutrition-ollama  | time=2026-07-23T23:03:14.008Z level=INFO source=model_list_cache.go:112 msg="model list cache hydration complete" models=1 failures=0 elapsed=2.412167ms
nutrition-ollama  | time=2026-07-23T23:03:14.058Z level=INFO source=types.go:50 msg="inference compute" id=cpu library=cpu compute="" name=cpu description=cpu libdirs=ollama driver="" pci_id="" type="" total="11.7 GiB" available="11.6 GiB"
nutrition-ollama  | time=2026-07-23T23:03:14.058Z level=INFO source=routes.go:2054 msg="vram-based default context" total_vram="0 B" default_num_ctx=4096
Container nutrition-ollama Waiting 
Container 4020aiserver-ollama-pull-1 Waiting 
nutrition-ollama  | time=2026-07-23T23:03:14.086Z level=INFO source=model_recommendations.go:177 msg="model recommendations cache sleep scheduled" wait=3h19m34.907531305s consecutive_failures=0
nutrition-ollama  | [GIN] 2026/07/23 - 23:03:17 | 200 |     109.792µs |      172.18.0.3 | HEAD     "/"
nutrition-ollama  | [GIN] 2026/07/23 - 23:03:17 | 200 |  398.845292ms |      172.18.0.3 | POST     "/api/pull"
pulling manifest 
ollama-pull-1     | pulling 74701a8c35f6: 100% ▕██████████████████▏ 1.3 GB                         
ollama-pull-1     | pulling 966de95ca8a6: 100% ▕██████████████████▏ 1.4 KB                         
ollama-pull-1     | pulling fcc5a6bec9da: 100% ▕██████████████████▏ 7.7 KB                         
ollama-pull-1     | pulling a70ff7e570d9: 100% ▕██████████████████▏ 6.0 KB                         
ollama-pull-1     | pulling 4f659a1e86d7: 100% ▕██████████████████▏  485 B                         
ollama-pull-1     | verifying sha256 digest 
ollama-pull-1     | writing manifest 
ollama-pull-1     | success 
Container 4020aiserver-ollama-pull-1 Exited 
ollama-pull-1 exited with code 0                                                                                                                                                                                                                                                                       
nutrition-ollama  | [GIN] 2026/07/23 - 23:03:24 | 200 |      22.084µs |       127.0.0.1 | HEAD     "/"
nutrition-ollama  | [GIN] 2026/07/23 - 23:03:24 | 200 |       230.5µs |       127.0.0.1 | GET      "/api/tags"
Container nutrition-ollama Healthy 
nutrition-web     |  * Serving Flask app 'main'
nutrition-web     |  * Debug mode: on
nutrition-web     | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
nutrition-web     |  * Running on http://127.0.0.1:5001
nutrition-web     | Press CTRL+C to quit
nutrition-web     |  * Restarting with stat
nutrition-web     |  * Debugger is active!
nutrition-web     |  * Debugger PIN: 109-018-946
nutrition-ollama  | [GIN] 2026/07/23 - 23:03:34 | 200 |        28.5µs |       127.0.0.1 | HEAD     "/"
nutrition-ollama  | [GIN] 2026/07/23 - 23:03:34 | 200 |       291.5µs |       127.0.0.1 | GET      "/api/tags"
```