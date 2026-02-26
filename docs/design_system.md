# 🎨 The Atelier Qin Design System (v1.0)
> *Engineering Taste. Crafting Silence. Building Truth.*

## 1. Core Philosophy (核心哲学)

**"Signal over Noise" (信号 > 噪音)**
*   **Minimalism is Security**: 极简不是为了好看，是为了防止注意力流失。
*   **Density is Power**: 我们不做留白过度的"登陆页"，我们做高密度的"控制台"。
*   **Grid is Law**: 所有元素必须对齐。如果不对齐，就是 Bug。
*   **Truth is Raw**: 不要美化数据。展示原始数字 (Mono Font)。

---

## 2. Design Tokens (设计令牌)

### 🎨 Colors (Zinc & Signal)
我们只使用 **Zinc (锌灰)** 作为基底，**Signal Colors** 作为功能点缀。

*   **Background**:
    *   `bg-zinc-950` (#09090b): **Main Void** (主背景)
    *   `bg-zinc-900` (#18181b): **Module Surface** (模块背景)
    *   `bg-black/20`: **Deep Void** (深层背景，用于输入框/终端)

*   **Borders**:
    *   `border-zinc-800`: **Structure** (结构线)
    *   `border-zinc-700`: **Active/Hover** (悬停线)
    *   `border-white/5`: **Subtle** (隐形分割)

*   **Typography**:
    *   `text-zinc-200`: **Primary Read** (正文)
    *   `text-white`: **Headlines** (标题)
    *   `text-zinc-500`: **Metadata** (标签/时间/次要信息)

*   **Signals (Functional)**:
    *   🟢 `text-emerald-500`: **Success / Live / Growth** (系统正常)
    *   🔴 `text-red-500`: **Error / Critical / Defcon** (系统警报)
    *   🟡 `text-amber-500`: **Warning / Code / Build** (构建中)
    *   🔵 `text-blue-500`: **Network / Cast / Link** (连接)
    *   🟣 `text-purple-500`: **Curation / Taste / Magic** (魔法/策展)

### 🔠 Typography (Geist Stack)
*   **Sans**: `Geist Sans` (UI / Reading) - *Modern, geometric, clean.*
*   **Mono**: `Geist Mono` (Data / Code / Labels) - *Technical, precise.*
*   **Scale**:
    *   `text-[10px] uppercase tracking-widest`: **Labels / Tags** (微标)
    *   `text-xs font-mono`: **Data Points** (数据)
    *   `text-sm leading-relaxed`: **UI Text** (界面)
    *   `text-base leading-7`: **Article Body** (文章)
    *   `text-4xl font-bold tracking-tight`: **Display Headers** (大标题)

### 📐 Spacing & Layout
*   **Grid**: 4px baseline. Tailwind default.
*   **Containers**:
    *   `max-w-5xl mx-auto px-6`: **Standard Dashboard**
    *   `max-w-2xl mx-auto px-6`: **Deep Reading**
*   **Glassmorphism**:
    *   `backdrop-blur-md bg-zinc-900/50 border border-white/5`

---

## 3. Component Patterns (组件模式)

### 📦 The Module (标准模块容器)
```tsx
<div className="bg-zinc-900/20 border border-zinc-800 rounded p-4 relative overflow-hidden group">
  {/* Top Accent Line */}
  <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-zinc-700 to-transparent opacity-20" />
  
  {/* Header */}
  <h3 className="text-[11px] text-zinc-500 uppercase tracking-widest mb-4 font-bold flex items-center gap-2">
    <Icon className="w-3 h-3" />
    MODULE TITLE
  </h3>
  
  {/* Content */}
  <div className="text-zinc-300 text-sm">...</div>
</div>
```

### 🏷️ The Signal Tag (信号标签)
```tsx
<span className="text-[9px] px-1.5 py-0.5 rounded border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 font-mono">
  LIVE
</span>
```

### 📟 The Data Row (数据行)
```tsx
<div className="flex justify-between items-center py-2 border-b border-white/5 font-mono text-xs">
  <span className="text-zinc-500">CPU_LOAD</span>
  <span className="text-emerald-500">12%</span>
</div>
```

---

## 4. Cursor/AI Rules (指令集)

> *把这段复制到 `.cursorrules` 或 AI 的 System Prompt 中。*

```markdown
# Atelier Qin Design System Rules

You are an expert Frontend Engineer specializing in "Swiss Style" and "Mission Control" interfaces.
Follow these strict design guidelines:

1.  **Color Palette**: Use ONLY Tailwind `zinc` colors for UI.
    -   Background: `bg-zinc-950`
    -   Border: `border-zinc-800`
    -   Text: `text-zinc-200` (primary), `text-zinc-500` (secondary)
    -   Accents: Emerald (Success), Amber (Warning), Blue (Info), Red (Critical). NO OTHER COLORS.

2.  **Typography**:
    -   Use `font-sans` for layout and `font-mono` for ANY numbers, dates, or technical data.
    -   All labels/headers (h3, h4) must be: `text-[10px] uppercase tracking-widest font-bold text-zinc-500`.

3.  **Layout & Effects**:
    -   Use `backdrop-blur` sparingly (only for overlays/sticky headers).
    -   Borders should be subtle (`border-zinc-800` or `border-white/5`).
    -   Use `group-hover` for subtle interactivity (e.g., border color change on hover).

4.  **Philosophy**:
    -   **Density**: Prefer compact, information-dense layouts over whitespace-heavy ones.
    -   **Rawness**: Show the data. Don't hide complexity, organize it.
    -   **Animation**: Use `framer-motion` for fast, crisp transitions (duration: 0.2s, ease: easeOut). No bouncy/springy animations.
```
