import os
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from git import Repo
import shutil
from urllib.parse import urlparse

app = Flask(__name__)

# Load secret key from environment variable (recommended)
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("Missing SECRET_KEY environment variable")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        repo_url = request.form.get('url')
        if not repo_url:
            flash("Please enter a GitHub repository URL.", "error")
            return redirect(url_for('index'))

        try:
            # Create a temporary directory for cloning
            with tempfile.TemporaryDirectory() as temp_dir:
                repo_directory = temp_dir

                # Extract repository name from the GitHub URL
                parsed_url = urlparse(repo_url)
                repo_name = os.path.splitext(os.path.basename(parsed_url.path))[0]

                # Clone the repository to the temporary directory
                Repo.clone_from(repo_url, repo_directory)

                # Create a ZIP file containing the cloned repository
                zip_filename = os.path.join(temp_dir, f"{repo_name}.zip")
                shutil.make_archive(zip_filename, 'zip', repo_directory)

                # Serve the ZIP file for download
                return send_file(zip_filename, as_attachment=True, attachment_filename=f"{repo_name}.zip")

        except GitCommandError as e:
            flash(f"Failed to clone repository: {e}", "error")
        except Exception as e:
            flash(f"An unexpected error occurred: {e}", "error")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
