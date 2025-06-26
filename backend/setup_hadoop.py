import os
import sys
import urllib.request
import shutil
import zipfile

def setup_hadoop_for_windows():
    """Configuration complète de Hadoop pour Windows"""
    
    print("📦 Configuration de l'environnement Hadoop pour Windows...")
    
    # Répertoire courant
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Créer le dossier hadoop s'il n'existe pas
    hadoop_dir = os.path.join(current_dir, "hadoop")
    bin_dir = os.path.join(hadoop_dir, "bin")
    
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)
    
    # URL pour télécharger winutils.exe
    winutils_url = "https://github.com/steveloughran/winutils/raw/master/hadoop-3.0.0/bin/winutils.exe"
    winutils_path = os.path.join(bin_dir, "winutils.exe")
    
    # Télécharger winutils.exe
    if not os.path.exists(winutils_path):
        try:
            print(f"⬇️ Téléchargement de winutils.exe depuis {winutils_url}...")
            urllib.request.urlretrieve(winutils_url, winutils_path)
            print("✅ winutils.exe téléchargé avec succès!")
        except Exception as e:
            print(f"❌ Erreur lors du téléchargement: {str(e)}")
            
            # Créer un fichier factice si le téléchargement échoue
            try:
                with open(winutils_path, 'wb') as f:
                    f.write(b'DUMMY FILE')
                print("⚠️ Fichier winutils.exe factice créé.")
            except Exception:
                pass
    
    # Configuration des variables d'environnement
    os.environ['HADOOP_HOME'] = hadoop_dir
    
    # Désactiver la fonctionnalité de sécurité problématique
    os.environ['JAVA_OPTS'] = '-Djavax.security.auth.useSubjectCredsOnly=false'
    os.environ['PYSPARK_SUBMIT_ARGS'] = '--conf spark.authenticate=false pyspark-shell'
    
    print(f"✅ HADOOP_HOME configuré: {hadoop_dir}")
    print("🔄 Configuration terminée!")
    print("Lancez maintenant 'python app.py'")
    
if __name__ == "__main__":
    setup_hadoop_for_windows()