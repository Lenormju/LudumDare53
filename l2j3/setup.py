from cx_Freeze import setup, Executable

buildOptions = dict(include_files=['assets/'])

setup(
      name="dEVILery",
      version="0.1",
      description="Jeu créé par la Kaizen Team L2J2R pour la Ludum Dare n°53",
      executables=[Executable("main.py")],
      options=dict(build_exe=buildOptions),
)
