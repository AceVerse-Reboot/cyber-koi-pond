# Publish Cyber Koi Pond

This package is ready to review and upload. It has not been published to GitHub by ChatGPT.

Recommended repository name: `cyber-koi-pond`

Description: An animated AI and cybersecurity themed pond for GitHub profiles, built on Anthony Yalong's git-koi.

Suggested topics: `github-profile`, `github-actions`, `generative-art`, `pixel-art`, `koi`, `python`, `cybersecurity`.

## Upload with Git (preserves the hidden workflow directory)

1. Extract the ZIP.
2. On https://github.com/new, create a **public** repository called `cyber-koi-pond`. Leave GitHub's README, licence and .gitignore options unticked; the package already includes these files.
3. Open the extracted `cyber-koi-pond` folder in VS Code, then open its terminal.
4. Run these commands. They publish all project files, so first check you are inside the extracted project folder:

   ```bash
   git init -b main
   git add .
   git commit -m "Initial release of Cyber Koi Pond"
   git remote add origin https://github.com/AceVerse-Reboot/cyber-koi-pond.git
   git push -u origin main
   ```

   GitHub may ask you to sign in through your usual Git credential manager. Never paste a token into a public file or post.

5. Open the repository's **Actions** tab. Confirm that the first pond workflow completes successfully. It will replace the bundled example with your current activity-based fish.
6. Confirm the README preview works. Optionally enable **Template repository** in Settings so others can use **Use this template**.
7. Once the repository is public and its workflow succeeds, use its public URL in your LinkedIn post. The LinkedIn draft is not included in this ZIP.

Your existing personal profile workflow does not need to be replaced to publish this separate project.

## Browser upload alternative

Upload the extracted project contents, not the ZIP itself. Ensure `.github/workflows/pond.yml` is present after uploading; your file picker may hide `.github`. If it was omitted, use **Add file → Create new file**, enter `.github/workflows/pond.yml`, and paste the matching local file's contents. The project uses its own `README.md`; do not copy it over your personal profile README.

## Validation completed before packaging

- Three automated tests passed for invalid configuration, preserving existing output on an empty input, and opaque looping GIF output.
- The renderer was run on the real git-koi input and generated all 180 frames.
- YAML files parsed successfully and the still preview was visually inspected.
- The remote composite-action workflow has not yet been run from the new repository; validate that first GitHub Actions run after publication.

## If GitHub skips .gitignore

The archive contains `.gitignore`. If the browser upload omits it, commit the other files first, then choose **Add file → Create new file**. Enter `.gitignore` as the filename and paste:

```gitignore
.neural-koi/
__pycache__/
*.pyc
.venv/
*.tmp.gif
```

Click **Commit changes**. Missing `.gitignore` does not stop the renderer working; it keeps temporary and local files out of later Git commits.

Also check that `.github/workflows/pond.yml` uploaded: this file is required for the automatic workflow. If it is missing, create it using that exact filename and copy the contents from the matching file in the extracted project.
