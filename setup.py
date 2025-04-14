#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import re

# Lire la version depuis le fichier __init__.py
with open(os.path.join('ghostnet', '__init__.py'), 'r') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        version = '0.1.0'  # Version par défaut

# Lire le contenu du README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ghostnet',
    version=version,
    description='GhostNet - Une solution de cybersécurité basée sur la déception et l\'IA pour la détection et l\'analyse des intrusions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='GhostNet Team',
    author_email='contact@ghostnet-security.com',
    url='https://github.com/servais1983/GhostNet',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        # Dépendances de base
        'Flask>=2.0.0',
        'Flask-RESTful>=0.3.9',
        'Flask-Cors>=3.0.10',
        'PyYAML>=6.0',
        'requests>=2.27.1',
        'python-dotenv>=0.19.2',
        
        # Dépendances pour le réseau
        'scapy>=2.4.5',
        'pyroute2>=0.6.7',
        'netfilterqueue>=1.0.0',
        'psutil>=5.9.0',
        
        # Dépendances pour l'IA
        'numpy>=1.22.0',
        'pandas>=1.4.0',
        'scikit-learn>=1.0.2',
        'tensorflow>=2.8.0',
        'torch>=1.11.0',
        
        # Dépendances pour la génération de leurres
        'Jinja2>=3.0.3',
        'faker>=11.3.0',
        
        # Dépendances pour la journalisation et le suivi
        'rich>=12.0.0',
        'colorama>=0.4.4',
        'tqdm>=4.62.3',
        
        # Dépendances pour la sécurité
        'cryptography>=36.0.1',
        'pyOpenSSL>=22.0.0',
        'bcrypt>=3.2.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'flake8>=4.0.1',
            'black>=22.1.0',
            'isort>=5.10.1',
            'mypy>=0.931',
            'sphinx>=4.4.0',
            'sphinx-rtd-theme>=1.0.0',
        ],
        'siem': [
            'elasticsearch>=8.0.0',
            'splunk-sdk>=1.6.18',
        ],
        'docker': [
            'docker>=5.0.3',
        ],
    },
    entry_points={
        'console_scripts': [
            'ghostnet=ghostnet.cli:main',
            'ghostnet-server=ghostnet.server:main',
            'ghostnet-lure=ghostnet.lure_generator.cli:main',
            'ghostnet-detect=ghostnet.detection.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: French',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Security',
        'Topic :: System :: Networking :: Monitoring',
    ],
    keywords='cybersecurity, honeypot, deception, intrusion detection, threat intelligence, ai',
    project_urls={
        'Documentation': 'https://ghostnet-security.com/docs',
        'Source': 'https://github.com/servais1983/GhostNet',
        'Issues': 'https://github.com/servais1983/GhostNet/issues',
    },
)
