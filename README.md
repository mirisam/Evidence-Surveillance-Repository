# Evidence Surveillance Hub Prototype

The Evidence Surveillance Hub is a Quarto-based prototype website for publishing outbreak evidence surveillance outputs. It provides outbreak-specific pages with searchable evidence tables, downloadable datasets, and automated updates through GitHub Actions and GitHub Pages.

## Live Website

[View the Evidence Surveillance Repository Site\](https://mirisam.github.io/Evidence-Surveillance-Repository/)

## Repository Contents

This repository contains the source files, outbreak-specific CSV datasets, optional downloadable Excel files, and deployment workflow used to generate the prototype website.

## Documentation

- [Developer documentation](docs/developer-documentation.md)
- [Update guide](update-guide.qmd)

## Basic Workflow

```text
Update CSV → Commit to GitHub → GitHub Actions rebuilds site → GitHub Pages updates live website
