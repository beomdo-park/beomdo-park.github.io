import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import warnings


def setup_korean_fonts():
    """
    Sets up Matplotlib to use Korean fonts (NanumGothic) based on the OS.
    """
    font_family_set = False
    try:
        os_name = platform.system()
        font_name_to_set = None

        if os_name == "Windows":
            font_name_to_set = (
                "NanumGothic"  # 사용자가 Windows에 나눔고딕을 설치했다고 가정
            )
        elif os_name == "Darwin":  # macOS
            font_name_to_set = "AppleGothic"
        elif os_name == "Linux":  # GitHub Actions 등
            # fonts-nanum 패키지가 설치되면 'NanumGothic' 이름으로 사용 가능해야 함
            font_name_to_set = "NanumGothic"

        if font_name_to_set:
            available_fonts = [f.name for f in fm.fontManager.ttflist]
            if font_name_to_set in available_fonts:
                plt.rc("font", family=font_name_to_set)
                font_family_set = True
            elif (
                os_name == "Linux" and "NanumSquare" in available_fonts
            ):  # Alternative Nanum font
                plt.rc("font", family="NanumSquare")
                font_name_to_set = "NanumSquare"
                font_family_set = True
            elif os_name == "Linux":
                # If specific Nanum fonts are not found by name, try to find any Nanum font
                nanum_fonts = [f for f in available_fonts if "Nanum" in f]
                if nanum_fonts:
                    plt.rc("font", family=nanum_fonts[0])
                    font_name_to_set = nanum_fonts[0]
                    font_family_set = True
                else:
                    warnings.warn(
                        f"'{font_name_to_set}' not found on {os_name}. Korean text may not render correctly. Ensure 'fonts-nanum' is installed and Matplotlib's cache is updated."
                    )
            else:
                warnings.warn(
                    f"'{font_name_to_set}' not found on {os_name}. Korean text may not render correctly."
                )

        plt.rcParams["axes.unicode_minus"] = False  # 마이너스 부호 깨짐 방지

        if font_family_set:
            print(
                f"Matplotlib font successfully set to '{font_name_to_set}' for Korean on {os_name}."
            )
        elif os_name != "Linux":  # Linux는 위에서 이미 경고했을 수 있음
            warnings.warn(
                f"Could not set a specific Korean font on {os_name}. Defaulting to system fonts. Korean text might not display correctly."
            )

    except Exception as e:
        warnings.warn(
            f"Error setting up Matplotlib font: {e}\\n"
            "Please ensure a Korean-supporting font is installed "
            "and Matplotlib's font cache is up-to-date."
        )


def set_rcparams(params: dict):
    """
    Set multiple Matplotlib rcParams from a dictionary.

    Args:
        params (dict): Dictionary of rcParams to set.
    """
    for key, value in params.items():
        plt.rcParams[key] = value


setup_korean_fonts()
set_rcparams(
    {
        "figure.figsize": (10, 6),  # Default figure size
        "figure.dpi": 100,  # Default DPI
        "axes.titlesize": "large",  # Title size for axes
        "axes.labelsize": "medium",  # Label size for axes
        "xtick.labelsize": "small",  # X-tick label size
        "ytick.labelsize": "small",  # Y-tick label size
    }
)
