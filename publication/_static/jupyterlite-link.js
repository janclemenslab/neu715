document.addEventListener("DOMContentLoaded", () => {
  const source = document.querySelector('.view-this-page a[href$=".ipynb"]');
  const themeToggles = document.querySelectorAll(".theme-toggle-container");
  if (!source || !themeToggles.length) return;

  const [root, notebook] = source.getAttribute("href").split("_sources/");
  if (!notebook) return;
  themeToggles.forEach((themeToggle) => {
    const link = document.createElement("a");
    link.className = "muted-link";
    link.href = `${root}lite/lab/index.html?path=${encodeURIComponent(notebook)}`;
    link.target = "_blank";
    link.rel = "noopener";
    link.title = "Open in JupyterLite";
    link.setAttribute("aria-label", "Open in JupyterLite");
    link.style.alignItems = "center";
    link.style.display = "flex";
    link.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"></path></svg>';
    themeToggle.insertAdjacentElement("beforebegin", link);
  });
});
