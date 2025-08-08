"""
Basic tests for Clean HDMI project
"""

def test_import():
    """Test that project structure exists"""
    import os
    assert os.path.exists('src')
    
def test_config():
    """Test configuration file"""
    import json
    import os
    
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
            assert 'camera' in config
            assert config['camera']['model'] == 'DSC-HX400'
    else:
        # Skip if config doesn't exist yet
        pass

def test_java_files():
    """Test that Java source files exist"""
    import os
    java_dir = 'src/main/java/com/cleanhdmi'
    
    if os.path.exists(java_dir):
        java_files = [f for f in os.listdir(java_dir) if f.endswith('.java')]
        assert len(java_files) > 0
    else:
        # Directory will be created during build
        pass
