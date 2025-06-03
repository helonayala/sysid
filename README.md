# SYSID: an introductory course on system identification

Welcome! This repository hosts the class notes for an introduction to the fundamental concepts of **system identification**.

To foster a **hands-on learning experience**, these notes include adaptable Python scripts. You're encouraged to build upon this **starter code**. 

Originally developed in MATLAB, the scripts have been translated to Python (with assistance from LLMs) and are now readily accessible online within these notes. 

Students can easily navigate the material and click the [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](YOUR_COLAB_NOTEBOOK_LINK_HERE) to start experimenting directly in their browser.

I hope you find this resource valuable. The methods are demonstrated using **real-world data**, allowing you to explore both the **potentialities and limitations** of the techniques discussed.

# Updating This Jupyter Book Site

This website is built using [Jupyter Book](https://jupyterbook.org/) from `.ipynb` notebooks and hosted on GitHub Pages. The update process is designed to be straightforward with automated builds using the direct Google Colab to GitHub integration.

## How to Update the Content

1.  **Edit Notebooks in Google Colab:**
    * Open the desired `.ipynb` notebook file (from this repository, typically after opening it from GitHub via Colab's "Open notebook" feature or having it in your Google Drive synced with your project) in [Google Colab](https://colab.research.google.com/).
    * Make your changes, run code cells, and save your work within Colab.

2.  **Push Updated Notebook(s) to GitHub (Directly from Colab):**
    * In Colab, go to `File -> Save a copy in GitHub`.
    * Select this repository.
    * Ensure you are committing to the correct branch (usually `main` or `master`).
    * Provide a clear commit message describing your changes. This will commit and push the updated notebook directly to the repository.

3.  **Automatic Website Rebuild and Deployment:**
    * Once your changes are pushed to the designated branch (e.g., `main`), a GitHub Actions workflow configured in this repository will automatically trigger.
    * This workflow will:
        1.  Checkout the latest code.
        2.  Install Jupyter Book and any dependencies listed in `requirements.txt`.
        3.  Rebuild the entire Jupyter Book.
        4.  Deploy the updated HTML site to GitHub Pages.
    * You can monitor the progress of this process in the "Actions" tab of this repository.

## Important Reminders & Prerequisites

* **GitHub Actions Workflow:** This automation relies on a workflow file (e.g., `.github/workflows/deploy.yml`) present in the repository.
* **GitHub Pages Configuration:** The repository's GitHub Pages settings must be configured to "Build and deployment" from **GitHub Actions**.
* **Table of Contents (`_toc.yml`):** If you **add a new notebook** or significantly restructure existing ones, you **MUST** update the `_toc.yml` file in the root of the repository to reflect these changes. Commit and push the updated `_toc.yml` (you might need to do this locally or via GitHub's web interface if you're not adding it through Colab's save).
* **Python Dependencies (`requirements.txt`):** If your notebooks start using **new Python libraries** that are necessary for the code within them to run, you **MUST** add these libraries (ideally with their versions, e.g., `pandas==2.0.3`) to the `requirements.txt` file in the root of this repository. Commit and push the updated `requirements.txt`. The GitHub Action uses this file to install the correct dependencies.
* **Build Time:** Allow a few minutes for the GitHub Action to complete and for the changes to be live on the GitHub Pages site.
* **Branch:** Ensure you are pushing changes (saving copies from Colab) to the branch that triggers the GitHub Actions workflow (typically `main` or `master`).

By following these steps, your class notes website will stay up-to-date with your latest edits.
