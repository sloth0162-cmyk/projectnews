def build_prompt(title, summary):
    return f"""
Title:
{title}

Summary:
{summary}

Create a cinematic editorial news illustration.

Rules:

- Understand the title and summary.
- Select the appropriate visual style based on the news topic.
- If about war, emphasize authentic military equipment, terrain, and atmosphere instead of graphic violence.
- If about anime, manga, cartoons, or animation, create premium anime artwork.
- If about a country, include its outline or recognizable landmarks subtly in the background while keeping the main subject as the focus.
- If about technology or AI, use futuristic laboratories, robots, chips, satellites, or digital elements.
- If about health, show hospitals, doctors, laboratories, or medical technology.
- If about business, represent finance, markets, factories, ports, or modern skylines.
- If about sports, capture peak action with dynamic motion.
- Otherwise create a symbolic editorial illustration representing the main idea.

Requirements:
Ultra detailed.
Professional editorial quality.
Magazine cover composition.
Cinematic lighting.
Depth of field.
HDR.
Volumetric lighting.
16:9.
No text.
No logo.
No watermark.
"""