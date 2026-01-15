# TODO: Fix All Project Issues

## Completed ✓

### YAML Fixes
- [x] Fix invalid YAML in creativity.yaml (removed merged `from typing import` section)
- [x] Ensure yaml.safe_load works correctly

### State Schema Fixes  
- [x] VideoState accurately reflects runtime state
- [x] Removed unused `image_path` key
- [x] Kept `frame_paths` as canonical image output
- [x] Added `shots`, `voice_s3_uri` keys

### Dead Code Removal
- [x] Removed legacy `render_cinematic_video` and `render_single_shot` from render_video.py
- [x] Disabled unused `planner_node` (marked as unused)
- [x] Disabled unused `generate_script.py` (marked as unused)
- [x] Disabled unused `generate_shots.py` (marked as unused)
- [x] Empty placeholder for graph/nodes/script.py

### FFmpeg Concat Fix
- [x] Fixed video_node to use `-f concat -safe 0` 
- [x] concat.txt now treated as concat demuxer format
- [x] Added validation for empty frames list

### Frame Evolution Quality
- [x] Added KEYFRAME_INTERVAL (8 frames) to prevent img2img degradation
- [x] Every 8th frame uses txt2img for fresh output
- [x] Lower img2img strength (0.35) for gradual evolution
- [x] Higher strength (0.65) for keyframes

### Prompt Variation
- [x] Added camera motion hints per frame (slow pan, push in, tilt, etc.)
- [x] enrich_prompt now accepts frame_num, total_frames, motion_hint
- [x] Temporal variation: "wide establishing shot", "transitioning view", "final composition"
- [x] Each frame gets unique camera/lighting/mood combo

### Pipeline Stability
- [x] Enabled attention slicing
- [x] Enabled VAE tiling  
- [x] Safe xformers fallback with warning
- [x] Added proper dtype handling (float16 for CUDA, float32 for CPU)
- [x] Comprehensive logging at each step

### Graph Correctness
- [x] LangGraph flow: prompt → image → voice → video
- [x] Only 4 active nodes (prompt, image, voice, video)
- [x] Unused nodes (planner, script) disabled

### Config Consistency
- [x] Model selection works via creative_router
- [x] Creativity config loads correctly
- [x] Prompt enrichment adds temporal variation
- [x] Single source of truth: prompts/prompt.py

## Final Expected Behavior ✓
- Each shot generates multiple evolving frames
- Frames stitched into single cinematic MP4
- Audio correctly synced
- No black frames, no silent failures, no broken YAML

