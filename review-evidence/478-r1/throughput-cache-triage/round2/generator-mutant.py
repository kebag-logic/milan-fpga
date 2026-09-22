import pathlib,sys
pathlib.Path(sys.argv[sys.argv.index('-o')+1]).write_text('INVALID_ROM_DATA\n')
