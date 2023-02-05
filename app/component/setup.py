import setuptools

setuptools.setup(
    name="streamlit_confetti",
    version="0.1.0",
    author="Ivan Sorokin",
    author_email="i.sorok1n@icloud.com",
    description="Streamlit Component wrapper on top of JSConfetti library",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.63",
    ],
)
