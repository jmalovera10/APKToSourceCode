import sys
import zipfile
import os
import shutil
import subprocess

# Get the apk path and name specified by user input
apk_path = sys.argv[1]
apk_path = apk_path.replace("\\", "/")
apk_name = apk_path.split("/")
apk_name = apk_name[len(apk_name) - 1]

# Delete the already generated source to prevent errors
if os.path.isdir("./exports/" + (apk_name.replace(".apk", "").replace(".", ""))):
    shutil.rmtree("./exports/" + (apk_name.replace(".apk", "").replace(".", "")))

# Apk file is copied to the generated folder
shutil.copy(apk_path, "./generated")
# The file is .apk file is parsed to .zip
if os.path.isdir("./generated/" + (apk_name.replace(".apk", ".zip"))):
    os.remove("./generated/" + (apk_name.replace(".apk", ".zip")))
os.rename("./generated/" + apk_name, "./generated/" + (apk_name.replace(".apk", ".zip")))

# Unzip process
zip_ref = zipfile.ZipFile("./generated/" + (apk_name.replace(".apk", ".zip")), 'r')
zip_ref.extractall("./generated/sources")
zip_ref.close()
os.remove("./generated/" + (apk_name.replace(".apk", ".zip")))

# DEX2JAR process
subprocess.call(["d2j-dex2jar.bat", "generated/sources/classes.dex", "--force"])

# Jar to source code using fernflower
subprocess.call(["java", "-jar", "decompiler.jar", "classes-dex2jar.jar",
                 "./exports/" + (apk_name.replace(".apk", "").replace(".", ""))])

# File deletion if exists to prevent errors
if os.path.isfile("./exports/" + (apk_name.replace(".apk", "").replace(".", ""))):
    shutil.rmtree("./exports/" + (apk_name.replace(".apk", "").replace(".", "")))

# XML files extraction from APK
subprocess.call(["java", "-jar", "apktool.jar", "d", apk_path, "-f"])
source = apk_name.replace(".apk", "")
xml_files = os.listdir(source)
for xml in xml_files:
    shutil.move(os.path.join(source, xml), "./exports/" + (apk_name.replace(".apk", "").replace(".", "")))
shutil.rmtree(source)

# RESULT IS EXPORTED TO EXPORTS
