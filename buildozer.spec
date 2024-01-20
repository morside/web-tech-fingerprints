[app]

# Title of your application
title = fingerprints

# Package name
package.name = org.kivy.fingerprints

# Package domain (needed for android/ios packaging)
package.domain = org.kivy

# Source code where the main.py lives
source.dir = .

# Source files to include (let empty to include all the files)
source.include_exts = py,png,gif,kv,atlas,txt,json,jpg

# Application versioning
version = 0.1

# Application requirements
requirements = python3,kivy,requests,dnspython

# Presplash of the application
presplash.filename = %(source.dir)s/src/assets/load.jpg

# Icon of the application
icon.filename = %(source.dir)s/src/assets/icon.png

# Supported orientations
orientation = portrait

# Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# Android specific
fullscreen = 0
android.api = 31
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a

# Bootstrap to use for android builds
p4a.bootstrap = sdl2
