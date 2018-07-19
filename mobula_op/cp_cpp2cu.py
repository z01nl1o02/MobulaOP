import os,shutil

cpp_exts = 'c,cpp,cxx'.split(',')
for root,pdirs,names in os.walk('src'):
    for name in names:
        sname,ext = os.path.splitext(name)
        if ext in cpp_exts:
            print 'skip {}'.format(os.path.join(root,name))
            continue
        shutil.copy(os.path.join(root,name), os.path.join(root,sname+'.cu'))
        print '{} done'.format( name )