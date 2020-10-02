
from setuptools import setup, find_packages 
    
long_description = 'A software to convert triangular meshes to course-grained LAMMPS molecular input files for Immersed Boundary problems.' 
  
setup( 
        name ='mesh2lammps', 
        version ='1.0.0', 
        author ='Mehdi Ataei, Erfan Pirmorad', 
        author_email ='ataei8@gmail.com, erfan.pirmorad.96@gmail.com', 
        url ='https://github.com/mehdiataei/mesh2lammps', 
        description ='To convert triangular meshes to course-grained LAMMPS molecular input.', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='MIT', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'mesh2lammps = src.mesh2lammps:main',
                'lammps2mesh = src.lammps2mesh:main'
            ] 
        }, 
        classifiers =( 
            "Programming Language :: Python :: 3", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ), 
        keywords ='triangular mesh course-grained LAMMPS python Immersed Boundary mesh2lammps', 
        install_requires=['trimesh','networkx'],
        zip_safe = False
) 
