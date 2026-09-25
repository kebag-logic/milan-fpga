VID73 fixture (reviewer-built, test-only): a copy of
configs/generated/endstation_arty_current/gen/ with only
`ADP_SRP_DOM_DEF_VID_C = 16'd2;` changed to `16'd73;`, passed to the
unchanged pp_shadow Makefile as
  SHAPE_1x1="+incdir+<copy-dir-parent> -CFLAGS -DDECLARATION_VID=73"
so the harness's own DECLARATION_VID expectation and the generated header
agree on a value that no hop defaults to.
