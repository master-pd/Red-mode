#!/bin/bash
# file: scripts/setup.sh

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                 MAR-PD v3.0 Installation                 ║"
echo "╚══════════════════════════════════════════════════════════╝"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo " Python3 not found! Installing..."
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install python3 python3-pip -y
    elif command -v yum &> /dev/null; then
        sudo yum install python3 python3-pip -y
    elif command -v pacman &> /dev/null; then
        sudo pacman -S python python-pip
    else
        echo "⚠️  Please install Python3 manually"
        exit 1
    fi
fi

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo " Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

# Install dependencies
echo " Installing Python dependencies..."
pip3 install -r requirements.txt

# Create necessary directories
echo " Creating directories..."
mkdir -p logs results cache data/{databases,wordlists}

# Set permissions
echo " Setting permissions..."
chmod +x scripts/*.sh

# Create default config if not exists
if [ ! -f "config.json" ]; then
    echo "⚙️  Creating default config..."
    cp config.example.json config.json
fi

echo ""
echo " Installation complete!"
echo ""
echo "To run MAR-PD:"
echo "  python3 main_runner.py"
echo "  or"
echo "  python3 mar_pd.py"
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║           Remember: Ethical Use Only!                    ║
      ╚══════════════════════════════════════════════════════════╝"