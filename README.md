# beomdo's ML-DL blog

데이터 분석, 머신러닝, 프로그래밍 관련 학습 내용을 기록하고 공유합니다.

[➡️ **블로그 바로가기**](https://beomdo-park.github.io)

## ✨ 기술 스택

[![Quarto](https://img.shields.io/badge/Quarto-4B8BBE?style=for-the-badge&logo=Quarto&logoColor=white)](https://quarto.org/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-181717?style=for-the-badge&logo=github&logoColor=white)](https://pages.github.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)

---

<!-- 추가적인 내용 (예: 최근 포스트, 연락처 등)은 여기에 추가할 수 있습니다. -->

## 🗂️ 레포지토리 구조

<svg width="520" height="420" xmlns="http://www.w3.org/2000/svg">
    <style>
        .bg { fill: #fcfcfc; }
        .folder-icon { fill: #FFCA28; stroke: #FFA000; stroke-width: 1; } /* 밝은 노란색 계열 */
        .file-icon { fill: #E0E0E0; stroke: #BDBDBD; stroke-width: 1; }   /* 밝은 회색 계열 */
        .output-folder-icon { fill: #AED581; stroke: #8BC34A; stroke-width: 1; } /* 연두색 계열 (docs) */
        .config-file-icon { fill: #B3E5FC; stroke: #4FC3F7; stroke-width: 1; } /* 하늘색 계열 (config) */
        .script-file-icon { fill: #CE93D8; stroke: #AB47BC; stroke-width: 1; } /* 연보라색 계열 (scripts) */
        .text-label { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; fill: #333; }
        .sub-text-label { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; fill: #555; }
        .desc-text-label { font-family: 'Segoe UI', Arial, sans-serif; font-size: 9px; fill: #777; } /* 설명용 텍스트 */
        .connector-line { stroke: #B0BEC5; stroke-width: 1.5; } /* 부드러운 회색 */
        .title-label { font-family: 'Segoe UI', Arial, sans-serif; font-size: 16px; font-weight: bold; fill: #263238; }
        /* 아이콘 모양 (간단한 폴더/파일 아이콘) */
        .folder-shape { transform: scale(0.8); }
        .file-shape { transform: scale(0.8); }
    </style>
    <rect x="0" y="0" width="100%" height="100%" class="bg"/>
    <!-- Root Folder -->
    <g transform="translate(20, 30)">
        <rect x="0" y="0" width="200" height="35" rx="5" class="folder-icon"/>
        <text x="100" y="23" text-anchor="middle" class="title-label">beomdo-park-blog/</text>
    </g>
    <!-- Connectors from Root -->
    <line x1="110" y1="65" x2="110" y2="90" class="connector-line"/> <!-- Vertical line from root center -->
    <!-- Level 1 Items - Folders -->
    <g transform="translate(10, 90)"> <!-- .github -->
        <line x1="55" y1="0" x2="100" y2="0" class="connector-line"/>
        <line x1="100" y1="0" x2="100" y2="-25" class="connector-line"/>
        <rect x="0" y="0" width="110" height="30" rx="4" class="folder-icon"/>
        <text x="55" y="16" text-anchor="middle" class="text-label">.github/</text>
        <text x="55" y="27" text-anchor="middle" class="desc-text-label">(GitHub 설정)</text>
        <line x1="55" y1="30" x2="55" y2="45" class="connector-line"/>
        <rect x="5" y="45" width="100" height="26" rx="3" class="folder-icon"/>
        <text x="55" y="58" text-anchor="middle" class="sub-text-label">workflows/</text>
        <text x="55" y="68" text-anchor="middle" class="desc-text-label">(자동화 작업)</text>
        <line x1="55" y1="71" x2="55" y2="86" class="connector-line"/>
        <rect x="15" y="86" width="80" height="22" rx="2" class="file-icon"/>
        <text x="55" y="97" text-anchor="middle" class="sub-text-label">publish.yml</text>
        <text x="55" y="106" text-anchor="middle" class="desc-text-label">(배포 스크립트)</text>
    </g>
    <g transform="translate(130, 90)"> <!-- posts -->
        <line x1="55" y1="0" x2="-20" y2="0" class="connector-line"/>
        <line x1="-20" y1="0" x2="-20" y2="-25" class="connector-line"/>
        <rect x="0" y="0" width="110" height="30" rx="4" class="folder-icon"/>
        <text x="55" y="16" text-anchor="middle" class="text-label">posts/</text>
        <text x="55" y="27" text-anchor="middle" class="desc-text-label">(블로그 게시글)</text>
        <line x1="55" y1="30" x2="55" y2="45" class="connector-line"/>
        <rect x="5" y="45" width="100" height="26" rx="3" class="folder-icon"/>
        <text x="55" y="58" text-anchor="middle" class="sub-text-label">[게시글 폴더]/</text>
        <text x="55" y="68" text-anchor="middle" class="desc-text-label">(주제별 폴더)</text>
        <line x1="55" y1="71" x2="55" y2="86" class="connector-line"/>
        <rect x="25" y="86" width="60" height="22" rx="2" class="file-icon"/>
        <text x="55" y="97" text-anchor="middle" class="sub-text-label">index.qmd</text>
        <text x="55" y="106" text-anchor="middle" class="desc-text-label">(게시글 내용)</text>
    </g>
    <g transform="translate(250, 90)"> <!-- scripts -->
        <line x1="55" y1="0" x2="-140" y2="0" class="connector-line"/>
        <line x1="-140" y1="0" x2="-140" y2="-25" class="connector-line"/>
        <rect x="0" y="0" width="110" height="30" rx="4" class="folder-icon"/>
        <text x="55" y="16" text-anchor="middle" class="text-label">scripts/</text>
        <text x="55" y="27" text-anchor="middle" class="desc-text-label">(보조 스크립트)</text>
        <line x1="55" y1="30" x2="55" y2="45" class="connector-line"/>
        <rect x="5" y="45" width="100" height="22" rx="2" class="script-file-icon"/>
        <text x="55" y="56" text-anchor="middle" class="sub-text-label">matplotlib_...</text>
        <text x="55" y="65" text-anchor="middle" class="desc-text-label">(폰트 설정 등)</text>
    </g>
    <!-- Level 1 Items - Key Files & Output Folder -->
    <line x1="110" y1="65" x2="380" y2="90" class="connector-line"/>
    <line x1="380" y1="90" x2="380" y2="330" class="connector-line"/> <!-- Vertical stem for files, 길이 조정 -->
    <g transform="translate(390, 100)"> <!-- _quarto.yml -->
        <line x1="0" y1="12" x2="-10" y2="12" class="connector-line"/>
        <rect x="0" y="0" width="120" height="28" rx="3" class="config-file-icon"/>
        <text x="60" y="15" text-anchor="middle" class="text-label">_quarto.yml</text>
        <text x="60" y="25" text-anchor="middle" class="desc-text-label">(Quarto 설정)</text>
    </g>
    <g transform="translate(390, 140)"> <!-- index.qmd -->
        <line x1="0" y1="12" x2="-10" y2="12" class="connector-line"/>
        <rect x="0" y="0" width="120" height="28" rx="3" class="file-icon"/>
        <text x="60" y="15" text-anchor="middle" class="text-label">index.qmd</text>
        <text x="60" y="25" text-anchor="middle" class="desc-text-label">(메인 페이지)</text>
    </g>
    <g transform="translate(390, 180)"> <!-- README.md -->
        <line x1="0" y1="12" x2="-10" y2="12" class="connector-line"/>
        <rect x="0" y="0" width="120" height="28" rx="3" class="file-icon"/>
        <text x="60" y="15" text-anchor="middle" class="text-label">README.md</text>
        <text x="60" y="25" text-anchor="middle" class="desc-text-label">(프로젝트 설명)</text>
    </g>
    <g transform="translate(390, 220)"> <!-- styles.css -->
        <line x1="0" y1="12" x2="-10" y2="12" class="connector-line"/>
        <rect x="0" y="0" width="120" height="28" rx="3" class="config-file-icon"/>
        <text x="60" y="15" text-anchor="middle" class="text-label">styles.css</text>
        <text x="60" y="25" text-anchor="middle" class="desc-text-label">(블로그 스타일)</text>
    </g>
    <g transform="translate(390, 260)"> <!-- docs/ -->
        <line x1="0" y1="12" x2="-10" y2="12" class="connector-line"/>
        <rect x="0" y="0" width="120" height="30" rx="4" class="output-folder-icon"/>
        <text x="60" y="16" text-anchor="middle" class="text-label">docs/</text>
        <text x="60" y="27" text-anchor="middle" class="desc-text-label">(빌드 결과)</text>
    </g>
</svg>

## 🚀 배포 과정

<svg width="700" height="420" xmlns="http://www.w3.org/2000/svg">
    <style>
        .container { fill: #f6f8fa; }
        .arrow { stroke: #586069; stroke-width: 1.5; fill: none; marker-end: url(#arrowhead); }
        .box { fill: #fff; stroke: #d1d5da; stroke-width: 1; rx: 6; ry: 6; }
        .text { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; fill: #24292e; text-anchor: middle; dominant-baseline: central; }
        .label { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; fill: #586069; text-anchor: middle; dominant-baseline: central; }
        .git-push-box { fill: #f6f8fa; stroke: #0366d6; }
        .branch-main-box { fill: #e6ffed; stroke: #28a745; }
        .workflow-file-box { fill: #f1f8ff; stroke: #0366d6; }
        .gh-actions-box { fill: #2088FF; stroke: #0366d6; }
        .branch-gh-pages-box { fill: #fffbdd; stroke: #f1e05a; }
        .blog-output-box { fill: #28a745; stroke: #1e7e34; }
        .blog-output-text { fill: #fff; }
    </style>
    <defs>
        <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="#586069" />
        </marker>
    </defs>
    <rect x="0" y="0" width="100%" height="100%" class="container"/>
    <!-- 1. Git Push -->
    <g transform="translate(150, 60)">
        <rect x="-70" y="-25" width="140" height="50" class="box git-push-box"/>
        <text x="0" y="-5" class="text">Git Push</text>
        <text x="0" y="12" class="label">(to main)</text>
    </g>
    <line x1="150" y1="85" x2="150" y2="110" class="arrow" />
    <!-- 2. Main Branch -->
    <g transform="translate(150, 140)">
        <rect x="-70" y="-25" width="140" height="50" class="box branch-main-box"/>
        <text x="0" y="-5" class="text">main branch</text>
        <text x="0" y="12" class="label">(Source Code)</text>
    </g>
    <line x1="220" y1="140" x2="270" y2="140" class="arrow" />
    <!-- 3. Workflow File -->
    <g transform="translate(350, 140)">
        <rect x="-70" y="-25" width="140" height="50" class="box workflow-file-box"/>
        <text x="0" y="-5" class="text">publish.yml</text>
        <text x="0" y="12" class="label">(.github/workflows)</text>
    </g>
    <line x1="350" y1="165" x2="350" y2="190" class="arrow" />
    <!-- 4. GitHub Actions -->
    <g transform="translate(350, 220)">
        <rect x="-70" y="-25" width="140" height="50" class="box gh-actions-box"/>
        <text x="0" y="-5" class="text blog-output-text">GitHub Actions</text>
        <text x="0" y="12" class="label blog-output-text">(CI/CD)</text>
    </g>
    <line x1="420" y1="220" x2="470" y2="220" class="arrow" />
    <!-- 5. gh-pages Branch -->
    <g transform="translate(550, 220)">
        <rect x="-70" y="-25" width="140" height="50" class="box branch-gh-pages-box"/>
        <text x="0" y="-5" class="text">gh-pages branch</text>
        <text x="0" y="12" class="label">(Build Output)</text>
    </g>
    <line x1="550" y1="245" x2="550" y2="270" class="arrow" />
    <!-- 6. GitHub Pages Blog -->
    <g transform="translate(550, 300)">
        <rect x="-70" y="-25" width="140" height="50" class="box blog-output-box"/>
        <text x="0" y="-5" class="text blog-output-text">Deployed Blog</text>
        <text x="0" y="12" class="label blog-output-text">(github.io)</text>
    </g>
</svg>

### 🔗 구조와 배포의 연결

이 블로그의 배포 과정은 위 두 다이어그램에 나타난 레포지토리 구조와 긴밀하게 연결되어 있습니다.

1.  **변경사항 발생 및 푸시**: 로컬에서 블로그 게시물(`posts/`)을 작성하거나, 스타일(`styles.css`), 또는 블로그 설정(`_quarto.yml`, `index.qmd`)을 수정한 후, 변경 사항을 `main` 브랜치로 `Git Push`합니다.
2.  **워크플로우 실행**: 이 푸시는 `.github/workflows/` 폴더 내의 `publish.yml` 파일에 정의된 GitHub Actions 워크플로우를 자동으로 트리거합니다.
3.  **빌드**: GitHub Actions는 `main` 브랜치의 최신 코드를 가져와 Quarto 프로젝트를 빌드합니다. 이 과정에서 `_quarto.yml`이 프로젝트 전체 설정을 담당하고, `posts/`의 `.qmd` 파일들이 개별 게시물로 변환됩니다. 필요한 경우 `scripts/` 내의 코드가 빌드 과정에 사용될 수 있습니다.
4.  **결과물 생성 및 배포**: 빌드가 완료되면, 생성된 웹사이트 파일들은 `docs/` 폴더 (레포지토리 구조 다이어그램의 '빌드 결과' 폴더)에 해당하는 내용으로 구성됩니다. `publish.yml` 워크플로우는 이 결과물을 `gh-pages` 브랜치로 푸시합니다.
5.  **블로그 게시**: GitHub Pages는 `gh-pages` 브랜치의 내용을 자동으로 감지하여 `https://beomdo-park.github.io` 주소로 블로그를 웹에 게시합니다.

이처럼 레포지토리의 각 구성 요소는 체계적인 배포 자동화 과정을 통해 최종적으로 여러분이 보시는 블로그로 완성됩니다.
