document.addEventListener("DOMContentLoaded", () => {
  const source = document.querySelector('.view-this-page a[href$=".ipynb"]');
  const themeToggles = document.querySelectorAll(".theme-toggle-container");
  if (!source || !themeToggles.length) return;

  const [root, notebook] = source.getAttribute("href").split("_sources/");
  if (!notebook) return;
  const githubNotebook = notebook.split("/").map(encodeURIComponent).join("/");
  const links = [
    {
      href: `https://mybinder.org/v2/gh/janclemenslab/neu715/main?urlpath=tree/${encodeURIComponent(`publication/${notebook}`)}`,
      label: "Open in MyBinder",
      icon: "B",
    },
    {
      href: `https://colab.research.google.com/github/janclemenslab/neu715/blob/main/publication/${githubNotebook}`,
      label: "Open in Google Colab",
      icon: "C",
    },
    {
      href: `${root}lite/lab/index.html?path=${encodeURIComponent(notebook)}`,
      label: "Open in JupyterLite",
      icon: '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"></path></svg>',
    },
  ];

  themeToggles.forEach((themeToggle) => {
    links.forEach(({ href, label, icon }) => {
    const link = document.createElement("a");
    link.className = "muted-link";
    link.href = href;
    link.target = "_blank";
    link.rel = "noopener";
    link.title = label;
    link.setAttribute("aria-label", label);
    link.style.alignItems = "center";
    link.style.display = "flex";
    link.innerHTML = icon;
    themeToggle.insertAdjacentElement("beforebegin", link);
    });
  });
});
