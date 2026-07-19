import os
import re
import glob

# Path setup
repo_dir = "/home/naman/Music/Jain-Naman-V"
resume_dir = os.path.join(repo_dir, "Resume")
readme_path = os.path.join(repo_dir, "README.md")

def main():
    # Find all PDF files in the Resume directory
    pdf_files = glob.glob(os.path.join(resume_dir, "*.pdf"))
    if not pdf_files:
        print("Error: No PDF files found in the Resume/ directory.")
        return

    # Find the latest file based on modification time
    latest_file = max(pdf_files, key=os.path.getmtime)
    latest_filename = os.path.basename(latest_file)
    print(f"Latest resume identified: {latest_filename}")

    # Read the current contents of README.md
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regular expression pattern to target the link inside the resume HTML placeholder block
    pattern = r"(<!-- START_RESUME_LINK -->\s*<a[^>]*href=\")([^\"]*)(\"[^>]*>.*?<!-- END_RESUME_LINK -->)"
    
    # Check if the placeholder pattern exists in README.md
    if not re.search(pattern, content, flags=re.DOTALL):
        print("Warning: Resume link placeholder comments (<!-- START_RESUME_LINK --> ... <!-- END_RESUME_LINK -->) not found in README.md.")
        return

    # Replace the old path with the new path
    new_content = re.sub(pattern, rf"\g<1>Resume/{latest_filename}\g<3>", content, flags=re.DOTALL)

    # Write changes back to README.md
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README.md updated successfully with the latest resume link.")

if __name__ == "__main__":
    main()
