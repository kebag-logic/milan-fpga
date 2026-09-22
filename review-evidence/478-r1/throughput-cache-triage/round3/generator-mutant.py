import pathlib,sys
pathlib.Path(sys.argv[sys.argv.index('-o')+1]+'.wrong-name').write_text('00000000\n')
