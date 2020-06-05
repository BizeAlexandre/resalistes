from cx_Freeze import setup, Executable
import sys

base = "Win32GUI"
#Remplacer "monprogramme.py" par le nom du script qui lance votre programme
executables = [Executable("listes6.py", base=base)]
#Renseignez ici la liste complète des packages utilisés par votre application
packages = ["idna","csv","time","operator","os","datetime","reportlab"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}



#Adaptez les valeurs des variables "name", "version", "description" à votre programme.
setup(
    name = "listes4",
    options = options,
    version = "0.1",
    description = 'transforme le fichier de réservation issu de Syracuse en fiches de commandes individuelles au format pdf',
    executables = executables
)
