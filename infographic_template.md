
# 🧬 Scientific Infographic Generation Template

---

## 🧾 TITLE & OVERALL STRUCTURE

A scientific infographic titled **“[TITLE]”**, centered at the top on one line.  
The image shows a **vertically exploded, isometric diagram** with exactly **[N] layers**, spaced evenly in **scale-accurate** order from top (largest) to bottom (smallest), against a **neutral grey background (RGB #CCCCCC)** with a **light grey isometric grid overlay**.

---

## 🔝 TOP LAYER — ORGANISM VISUAL + FUNCTION

- The top layer is a **high-resolution, photo-realistic, full-color image** of the organism **“[ORGANISM]”** from the JSON.  
- It is shown in **isometric view**, aligned with the orientation of all lower layers.  
- The organism appears **isolated** — no natural or photographic environment, just the grey background.  
- ✅ Must look **photographic**, **naturalistic**, and **realistic**  
- 🚫 No cartoon, stylized, artistic, or 3D-rendered imagery  
- 🚫 No environmental scenes (e.g., desert, leaf, water, landscape)  

> **Note:** This layer is the **largest** and includes **no caption or scale label**.

---

## 📚 LAYERS (Functional Components, Top to Bottom)

Each layer corresponds to a `functional_component` in the JSON.  
For each one:

### 1. [LAYER NAME]
- **Visual**:  
  - Draw using **black linework only** — clean, minimal, architectural-style  
  - Must follow **scientifically accurate structure** (based on microscope/literature references)  
  - Render in **isometric alignment**  
  - 🚫 No shading, no 3D rendering, no color  

- **Function Caption**:  
  - Position: **Left** of the layer  
  - Alignment: **Left-aligned**, outside the visual box  
  - Format: `"[Short function summary]"`  

- **Scale Label**:  
  - Position: **Right** of the layer  
  - Format: e.g., `"200 µm"`  
  - Connected to a **white vertical scientific ruler** with **logarithmic tick marks**

---

## 🎨 VISUAL STYLE & RULES

- **Background**:  
  - Flat grey (`RGB #CCCCCC`)  
  - With light grey **isometric grid** (engineering blueprint style)

- **Ruler**:  
  - Positioned on the **right side**  
  - Vertical, white background, black tick marks (logarithmic scale)

- **Alignment Lines**:  
  - Thin, vertical black lines connecting the center of all layers

- **Spacing**:  
  - Equal vertical spacing between layers  
  - **Layer sizes must strictly decrease** from top to bottom, reflecting **true scientific scale hierarchy**

- **Font**:  
  - Uniform **sans-serif**, small size  
  - No overlapping with visuals  
  - **Title**: centered and bold  
  - **All other text**: regular weight

---

## 🚫 DO NOT INCLUDE:

- Any background behind the organism (no sand, water, plants, etc.)  
- 3D rendered geometry, shading, drop shadows, or lighting effects  
- Color in any layer **except** the organism  
- Stylized, artistic, or symbolic representations  
- Captions on the right or **inside** diagrams  
- Layer sizes out of scientific order (no arbitrary scaling)
