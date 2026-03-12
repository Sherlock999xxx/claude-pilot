import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebars: SidebarsConfig = {
  docsSidebar: [
    "intro",
    {
      type: "category",
      label: "Getting Started",
      collapsed: false,
      items: [
        "getting-started/prerequisites",
        "getting-started/installation",
      ],
    },
    {
      type: "category",
      label: "Workflows",
      collapsed: false,
      items: [
        "workflows/sync",
        "workflows/spec",
        "workflows/quick-mode",
        "workflows/learn",
      ],
    },
    {
      type: "category",
      label: "Features",
      collapsed: false,
      items: [
        "features/share",
        "features/hooks",
        "features/context-preservation",
        "features/rules",
        "features/model-routing",
      ],
    },
    {
      type: "category",
      label: "Tools",
      collapsed: false,
      items: [
        "tools/mcp-servers",
        "tools/language-servers",
        "tools/console",
        "tools/cli",
      ],
    },
    {
      type: "category",
      label: "Reference",
      collapsed: false,
      items: ["reference/open-source"],
    },
  ],
};

export default sidebars;
