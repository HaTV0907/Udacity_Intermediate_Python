# Tesed on Ubuntu
    $ uname -a
    Linux katana 6.5.0-41-generic #41~22.04.2-Ubuntu SMP PREEMPT_DYNAMIC Mon Jun  3 11:32:55 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
# Clone source code
    $ git clone https://github.com/HaTV0907/Udacity_Intermediate_Python.git
# Update font
    # if your local machine does not have font, copy * from font folder to /usr/share/fonts/truetype
# Create virtual environment
    $ cd Udacity_Intermediate_Python/Meme_Generator
    # create virtual env
    $ python3 -m venv .venv
    # activate virtual env
    $ . .venv/bin/activate
# Install Xpdf
    # to read pdf file
    $ sudo apt-get install -y xpdf
# Install python-docx
    # to read docx file
    $ pip install python-docx
# Install Flask
    $ pip install Flask
# Install Requests
    $ pip install requests
# Install Pillow
    $ pip install pillow