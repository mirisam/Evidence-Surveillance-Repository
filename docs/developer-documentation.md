## Developer Documentation: Evidence Surveillance Hub Prototype

This repository contains a Quarto-based static website for publishing outbreak evidence surveillance outputs. The site is built with Quarto, hosted through GitHub Pages, and deployed automatically using GitHub Actions.

The purpose of the project is to provide a searchable, downloadable, and maintainable public-facing interface for outbreak-specific evidence surveillance datasets.

---

## Technology Stack

* **Quarto**: Static site generation
* **Observable JavaScript (OJS)**: Interactive CSV loading, searching, filtering, and table display
* **GitHub Pages**: Static site hosting
* **GitHub Actions**: Automated rendering and deployment
* **CSV files**: Source data for outbreak evidence tables
* **XLSX files**: Optional full datasets for end-user download
* **CSS**: Custom styling for cards, tables, filters, buttons, and page layout

---

## Repository Structure

```text
Evidence-Surveillance-Hub-prototype/
├── _quarto.yml
├── index.qmd
├── outbreaks.qmd
├── methods.qmd
├── update-guide.qmd
├── styles.css
├── _recent-updates.md
├── scripts/
│   └── generate_recent_updates.py
├── outbreaks/
│   ├── mpox/
│   │   ├── index.qmd
│   │   └── data/
│   │       └── references.csv
│   ├── hantavirus/
│   │   ├── index.qmd
│   │   ├── background/
│   │   │   └── index.qmd
│   │   └── data/
│   │       └── references.csv
│   └── bundibugyo-ebola/
│       ├── index.qmd
│       └── data/
│           ├── references.csv
│           └── full-dataset.xlsx
└── .github/
    └── workflows/
        └── publish.yml
```

---

## Site Configuration

The main Quarto site configuration is stored in:

```text
_quarto.yml
```

This file controls the website title, navigation bar, search settings, theme, footer, and custom CSS.

The site uses:

```yaml
project:
  type: website
```

and applies global styling through:

```yaml
format:
  html:
    theme: cosmo
    css: styles.css
```

---

## Homepage

The homepage is defined in:

```text
index.qmd
```

It includes:

* A project introduction
* A prototype banner
* A “Recently Updated” section
* A summary of the site purpose
* A high-level workflow description
* Links to key pages

The homepage includes the generated `_recent-updates.md` file using a Quarto include shortcode. This file is regenerated during deployment by `scripts/generate_recent_updates.py`.

---

## Outbreak Directory

The outbreak directory is defined in:

```text
outbreaks.qmd
```

Each outbreak is displayed as a card using Quarto div syntax:

```markdown
::: {.info-card}
### Hantavirus

Evidence surveillance data and background information for Hantavirus literature.

[View evidence](outbreaks/hantavirus/)  
[View background](outbreaks/hantavirus/background/)
```
## Outbreak Pages

Each outbreak has its own folder under:

```text
outbreaks/
```
Each outbreak page must include an:

```text
index.qmd
```

and a data file located at:

```text
data/references.csv
```

Example:
```text
outbreaks/bundibugyo-ebola/index.qmd
outbreaks/bundibugyo-ebola/data/references.csv
```
The outbreak page uses OJS to load the CSV file:

```text
rawReferences = FileAttachment("data/references.csv").csv({typed: false})
```

The page then detects available columns dynamically:

```text
visibleColumns = rawReferences.length > 0
  ? Object.keys(rawReferences[0]).filter(c =>
      c &&
      c.trim() !== "" &&
      !/^_+$/.test(c.trim()) &&
      !c.startsWith("__") &&
      !c.toLowerCase().startsWith("unnamed")
    )
  : []
```
This allows each outbreak CSV to have a different structure while still rendering in the same generic viewer.

## Search and Filtering

Each outbreak page includes a global search input:

```text
viewof searched_references = Inputs.search(
  references,
  {placeholder: "Search all fields..."}
)
```
Optional filters can be generated from the available CSV columns. The filter system uses the detected column names and creates dropdowns based on unique values in each column.

Filtered results are displayed using:

```text
Inputs.table(filtered_references, {
  columns: visibleColumns,
  height: 700,
  select: false
})
```
The table displays all visible columns in the CSV unless the page is customized to display a selected subset.

## Link Formatting for DOI and URL Columns

The table supports clickable links for DOI and URL columns using the format option in Inputs.table().

```text
format: {
  URL: value =>
    value
      ? htl.html`<a href=${value} target="_blank" rel="noopener noreferrer">View link</a>`
      : "",

  DOI: value =>
    value
      ? htl.html`<a href=${`https://doi.org/${value}`} target="_blank" rel="noopener noreferrer">${value}</a>`
      : ""
}
```
For this to work, the CSV should use the exact column names:

```text
DOI
URL
```

## Downloadable Data

Each outbreak page may include download buttons for both a public-facing CSV and a full Excel dataset.

Example:

```text
<div class="download-buttons">
<a href="data/references.csv" download="bundibugyo-ebola-key-columns.csv" class="btn btn-primary">
Download key columns CSV
</a>

<a href="data/full-dataset.xlsx" download="bundibugyo-ebola-full-dataset.xlsx" class="btn btn-primary">
Download full Excel dataset
</a>
</div>
```

The CSV is used for the website table. The Excel file is optional and can be used to provide the full dataset with Excel filters and formatting preserved.

## Recently Updated Automation

The homepage “Recently Updated” section is generated automatically by:

```text
scripts/generate_recent_updates.py
```

The script scans outbreak folders for:

```text
outbreaks/*/data/references.csv
```

It retrieves the most recent Git commit date for each dataset and writes the output to:

```text
_recent-updates.md
```
This file is then included in index.qmd.

The automation runs during the GitHub Actions deployment workflow before Quarto renders the site.

## GitHub Actions Deployment

Deployment is controlled by:

```text
.github/workflows/publish.yml
```
The workflow:

 - Checks out the repository
- Sets up Quarto
- Runs the recent updates generation script
- Renders the Quarto site
- Uploads the rendered _site directory
- Deploys the site to GitHub Pages

Key workflow section:

Steps:
  - Check out repository
```text
actions/checkout@v4
    with:
      fetch-depth: 0
```

  - Set up Quarto
```text
uses: quarto-dev/quarto-actions/setup@v2
```
  - Generate recent updates

```text
run: python scripts/generate_recent_updates.py
```
  - Render Quarto site
```text
uses: quarto-dev/quarto-actions/render@v2
```
  - Upload site artifact
```text
uses: actions/upload-pages-artifact@v3
    with:
      path: _site
```
The fetch-depth: 0 setting is required so the recent updates script can access Git history.

## Adding a New Outbreak

To add a new outbreak:

Create a new folder under 
```text
outbreaks/.
```
Example:

```text
outbreaks/measles/
```
Add an outbreak page:
```text
outbreaks/measles/index.qmd
```
Add the dataset:
```text
outbreaks/measles/data/references.csv
```
Add a card to outbreaks.qmd:
```text
::: {.info-card}
### Measles

Evidence surveillance table for measles literature.

[View evidence table](outbreaks/measles/)
:::
```
Commit the changes and wait for GitHub Actions to rebuild the site.

## Updating an Existing Outbreak

To update an existing outbreak dataset:

Prepare the updated CSV.
Rename it exactly:
```text
references.csv
```
Replace the existing file in the relevant outbreak folder:
```text
outbreaks/[outbreak-name]/data/references.csv
```
Commit the change.
Wait for GitHub Actions to rebuild the site.

The outbreak page and the homepage “Recently Updated” section will update automatically.

## Styling

Custom styling is stored in:

```text
styles.css
```
This file controls:

- Navbar/logo sizing
- Homepage hero section
- Card layouts
- Evidence table styling
- Table header colours
- Filter panel styling
- Download button layout
- Background information tables

Evidence tables are styled through selectors such as:
```text
.observablehq table th
.observablehq table td
```
Custom background-page tables use classes such as:
```text
.hanta-table
.comparison-table
.filter-panel
.download-buttons
```
## Data Governance Notes

Files in a public GitHub repository are publicly accessible. Folder-level privacy is not supported in a public repository. Any internal, confidential, sensitive, or non-approved files should not be committed to the public repository.

Recommended structure:
```text
Public repository:
- public-facing website pages
- approved references.csv files
- approved downloadable datasets

Private/internal storage:
- working datasets
- internal screening files and SOPs
```
Once a file has been committed publicly, deleting it later may not fully remove it from Git history.

## Design Principle

The site is designed around a low-maintenance workflow:
```text
Update CSV → Commit to GitHub → GitHub Actions rebuilds site → GitHub Pages updates live website
```
