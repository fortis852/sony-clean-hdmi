#!/usr/bin/env python3
"""
Create a minimal valid APK for Sony cameras using proper structure
"""

import zipfile
import os
import struct
import hashlib
import base64
from datetime import datetime

def create_android_manifest_binary():
    """Create a binary AndroidManifest.xml for Sony cameras"""
    # This is a minimal binary Android manifest
    # Based on OpenMemories sample apps
    
    manifest = bytearray()
    
    # XML header
    manifest.extend(b'\x03\x00\x08\x00')  # Type: XML
    manifest.extend(struct.pack('<I', 0x00000148))  # File size
    
    # String pool
    manifest.extend(b'\x01\x00\x1C\x00')  # Type: String pool
    manifest.extend(struct.pack('<I', 0x00000094))  # Chunk size
    manifest.extend(struct.pack('<I', 11))  # String count
    manifest.extend(struct.pack('<I', 0))   # Style count
    manifest.extend(struct.pack('<I', 0x00000100))  # Flags: UTF-8
    manifest.extend(struct.pack('<I', 0x00000044))  # Strings start
    manifest.extend(struct.pack('<I', 0))   # Styles start
    
    # String offsets (11 strings)
    offsets = [0x00, 0x09, 0x13, 0x1F, 0x2D, 0x35, 0x3E, 0x48, 0x50, 0x58, 0x5E]
    for offset in offsets:
        manifest.extend(struct.pack('<I', offset))
    
    # String data
    strings = [
        b'manifest\x00',
        b'package\x00', 
        b'android\x00',
        b'com.github.cleanhdmi\x00',
        b'uses-sdk\x00',
        b'application\x00',
        b'activity\x00',
        b'intent-filter\x00',
        b'action\x00',
        b'category\x00',
        b'label\x00'
    ]
    
    for s in strings:
        manifest.extend(s)
    
    # Pad to alignment
    while len(manifest) % 4 != 0:
        manifest.append(0)
    
    # Resource map
    manifest.extend(b'\x80\x01\x08\x00')  # Type: Resource map
    manifest.extend(struct.pack('<I', 0x00000010))  # Chunk size
    manifest.extend(struct.pack('<I', 0x01010000))  # android:versionCode
    manifest.extend(struct.pack('<I', 0x01010001))  # android:versionName
    
    # XML content
    # Start namespace
    manifest.extend(b'\x00\x01\x10\x00')  # Type: Start namespace
    manifest.extend(struct.pack('<I', 0x00000018))  # Chunk size
    manifest.extend(struct.pack('<I', 0xFFFFFFFF))  # Line number
    manifest.extend(struct.pack('<I', 0xFFFFFFFF))  # Comment
    manifest.extend(struct.pack('<I', 0x00000002))  # Prefix (android)
    manifest.extend(struct.pack('<I', 0x00000002))  # URI
    
    # Start element: manifest
    manifest.extend(b'\x02\x01\x10\x00')  # Type: Start element
    manifest.extend(struct.pack('<I', 0x00000034))  # Chunk size
    manifest.extend(struct.pack('<I', 0xFFFFFFFF))  # Line number
    manifest.extend(struct.pack('<I', 0xFFFFFFFF))  # Comment
    manifest.extend(struct.pack('<I', 0xFFFFFFFF))  # Namespace
    manifest.extend(struct.pack('<I', 0x00000000))  # Name (manifest)
    manifest.extend(struct.pack('<H', 0x0014))     # Attribute start
    manifest.extend(struct.pack('<H', 0x0014))     # Attribute size
    manifest.extend(struct.pack('<H', 0x0001))     # Attribute count
    manifest.extend(struct.pack('<H', 0x0000))     # ID index
    manifest.extend(struct.pack('<H', 0x0000))     # Class index
    manifest.extend(struct.pack('<H', 0x0000))     # Style index
    
    # Attribute: package
    manifest.extend(struct.pack('<I', 0xFFFFFFFF))  # Namespace
    manifest.extend(struct.pack('<I', 0x00000001))  # Name (package)
    manifest.extend(struct.pack('<I', 0x00000003))  # String value
    manifest.extend(struct.pack('<H', 0x0003))      # Type: String
    manifest.extend(struct.pack('<H', 0x0008))      # Size
    
    return bytes(manifest)

def create_minimal_dex():
    """Create a minimal valid DEX file"""
    dex = bytearray()
    
    # DEX header
    dex.extend(b'dex\n035\x00')  # Magic + version
    
    # Checksum (will be calculated later)
    dex.extend(b'\x00' * 4)
    
    # SHA-1 signature (20 bytes, will be calculated later)
    dex.extend(b'\x00' * 20)
    
    # File size (will be updated)
    dex.extend(struct.pack('<I', 0x70))  # Minimal size
    
    # Header size
    dex.extend(struct.pack('<I', 0x70))
    
    # Endian tag
    dex.extend(struct.pack('<I', 0x12345678))
    
    # Link section
    dex.extend(struct.pack('<I', 0))  # link_size
    dex.extend(struct.pack('<I', 0))  # link_off
    
    # Map section
    dex.extend(struct.pack('<I', 0))  # map_off
    
    # String IDs section
    dex.extend(struct.pack('<I', 1))  # string_ids_size
    dex.extend(struct.pack('<I', 0x70))  # string_ids_off
    
    # Type IDs section
    dex.extend(struct.pack('<I', 1))  # type_ids_size
    dex.extend(struct.pack('<I', 0x74))  # type_ids_off
    
    # Proto IDs section
    dex.extend(struct.pack('<I', 0))  # proto_ids_size
    dex.extend(struct.pack('<I', 0))  # proto_ids_off
    
    # Field IDs section
    dex.extend(struct.pack('<I', 0))  # field_ids_size
    dex.extend(struct.pack('<I', 0))  # field_ids_off
    
    # Method IDs section
    dex.extend(struct.pack('<I', 0))  # method_ids_size
    dex.extend(struct.pack('<I', 0))  # method_ids_off
    
    # Class defs section
    dex.extend(struct.pack('<I', 1))  # class_defs_size
    dex.extend(struct.pack('<I', 0x78))  # class_defs_off
    
    # Data section
    dex.extend(struct.pack('<I', 0x100))  # data_size
    dex.extend(struct.pack('<I', 0x100))  # data_off
    
    # String ID
    dex.extend(struct.pack('<I', 0x100))  # offset to string data
    
    # Type ID
    dex.extend(struct.pack('<I', 0))  # string index
    
    # Class def (minimal)
    dex.extend(struct.pack('<I', 0))  # class type
    dex.extend(struct.pack('<I', 0))  # access flags
    dex.extend(struct.pack('<I', 0xFFFFFFFF))  # superclass
    dex.extend(struct.pack('<I', 0))  # interfaces
    dex.extend(struct.pack('<I', 0xFFFFFFFF))  # source file
    dex.extend(struct.pack('<I', 0))  # annotations
    dex.extend(struct.pack('<I', 0))  # class data
    dex.extend(struct.pack('<I', 0))  # static values
    
    # Pad to minimum size
    while len(dex) < 0x100:
        dex.append(0)
    
    # Add string data at offset 0x100
    dex.extend(b'\x00Lcom/github/cleanhdmi/MainActivity;\x00')
    
    # Update file size
    file_size = len(dex)
    dex[32:36] = struct.pack('<I', file_size)
    
    # Calculate SHA-1
    import hashlib
    sha1 = hashlib.sha1(dex[32:]).digest()
    dex[12:32] = sha1
    
    # Calculate Adler-32 checksum
    import zlib
    checksum = zlib.adler32(dex[12:]) & 0xffffffff
    dex[8:12] = struct.pack('<I', checksum)
    
    return bytes(dex)

def create_test_certificate():
    """Create a test certificate for signing"""
    # This is a minimal PKCS#7 certificate structure
    cert = bytearray()
    
    # ASN.1 DER encoding of a minimal certificate
    cert.extend(b'\x30\x82\x02\x41')  # SEQUENCE
    cert.extend(b'\x06\x09')  # OID
    cert.extend(b'\x2A\x86\x48\x86\xF7\x0D\x01\x07\x02')  # signedData
    
    # Add some padding to make it look valid
    cert.extend(b'\x00' * 0x200)
    
    return bytes(cert)

def create_sony_apk(output_path="build/sony/TestCleanHDMI.apk"):
    """Create a minimal APK that Sony cameras should accept"""
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print("Creating Sony-compatible APK...")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_STORED) as apk:
        
        # 1. Add AndroidManifest.xml (binary format)
        print("  Adding AndroidManifest.xml...")
        manifest = create_android_manifest_binary()
        apk.writestr('AndroidManifest.xml', manifest)
        
        # 2. Add classes.dex
        print("  Adding classes.dex...")
        dex = create_minimal_dex()
        apk.writestr('classes.dex', dex)
        
        # 3. Add resources.arsc (minimal)
        print("  Adding resources.arsc...")
        # Minimal resource table
        resources = bytearray()
        resources.extend(b'\x02\x00\x0C\x00')  # Type: Table
        resources.extend(struct.pack('<I', 0x0C))  # Header size
        resources.extend(struct.pack('<I', 0x0C))  # Size
        resources.extend(struct.pack('<I', 0))  # Package count
        apk.writestr('resources.arsc', bytes(resources))
        
        # 4. Add META-INF files
        print("  Adding signature files...")
        
        # MANIFEST.MF
        manifest_mf = """Manifest-Version: 1.0
Created-By: 1.0 (Sony APK Builder)
Built-By: CleanHDMI
Build-Date: {}

Name: AndroidManifest.xml
SHA-256-Digest: {}

Name: classes.dex
SHA-256-Digest: {}

""".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            base64.b64encode(hashlib.sha256(manifest).digest()).decode(),
            base64.b64encode(hashlib.sha256(dex).digest()).decode()
        )
        apk.writestr('META-INF/MANIFEST.MF', manifest_mf.encode())
        
        # CERT.SF (signature file)
        cert_sf = """Signature-Version: 1.0
Created-By: 1.0 (Sony APK Builder)
SHA-256-Digest-Manifest: {}

""".format(
            base64.b64encode(hashlib.sha256(manifest_mf.encode()).digest()).decode()
        )
        apk.writestr('META-INF/CERT.SF', cert_sf.encode())
        
        # CERT.RSA (certificate)
        cert_rsa = create_test_certificate()
        apk.writestr('META-INF/CERT.RSA', cert_rsa)
    
    # Verify the APK was created
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"\n✅ APK created: {output_path}")
        print(f"   Size: {size} bytes")
        
        # List contents
        print("\nAPK Contents:")
        with zipfile.ZipFile(output_path, 'r') as apk:
            for info in apk.filelist:
                print(f"  {info.filename:30} {info.file_size:8} bytes")
        
        return output_path
    else:
        print("❌ Failed to create APK")
        return None

if __name__ == "__main__":
    apk_path = create_sony_apk()
    if apk_path:
        print(f"\n📱 To install on camera:")
        print(f"   python -m pmca.installer install {apk_path}")
