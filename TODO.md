# TODO: Fix All Project Issues

## Completed ✓

- [x] 1. Uncomment TTS in requirements.txt (added `coqui-tts`)
- [x] 2. Fix image extension (jpeg → jpg) in prompts/prompt.py
- [x] 3. Add voice node to graph (update graph.py) - now: prompt → image → voice → video
- [x] 4. Fix frame flattening in video_node (nested list → flat list)
- [x] 5. Fix /workspace/tmp/ paths to use /tmp/ instead (in video.py, voice.py, s3.py)
- [x] 6. Fix config file paths in model_registry.py and creative_router.py (use absolute paths)
- [x] 7. Create TMP_DIR and ensure directories exist with os.makedirs()
- [x] 8. Fix syntax error in s3.py (missing `import` keyword)
- [x] 9. Fix graph/graph.py - use VideoState type instead of dict, import from graph.state
- [x] 10. Fix graph/state.py - add missing fields (shots, frame_paths, voice_s3_uri)
- [x] 11. Fix scripts/render_video.py - change /workspace/tmp/ to /tmp/cofeposa/
- [x] 12. Fix prompts/prompt.py - use absolute path for image_s3 (file:// scheme)
- [x] 13. Fix scripts/generate_voice.py - remove unsupported --duration argument from TTS command
- [x] 14. Fix graph/nodes/image.py - add comprehensive logging and error handling for image generation
- [x] 15. Fix scripts/generate_image.py - add logging and error handling for SD pipeline
- [x] 16. Syntax validation passed for all Python files

## Pipeline Successfully Tested! 🎉

