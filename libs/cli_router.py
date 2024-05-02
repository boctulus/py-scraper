#
# CLI Router by Boctulus
#

def main(argv):
	 # Verificar si hay al menos un argumento
	if len(argv) < 1:
		return

	fn = argv[0]
	params = argv[1:]

	function = eval(fn)

	arr_args  = []
	arr_kargs = []
	for p in params:
		kv = p.split('=')
		if (kv.__len__() == 2):
			[key, val] = kv
			arr_kargs.append(f"{key}='{val}'")
		elif (kv.__len__() == 1):
			arr_args.append(f"'{kv[0]}'")	
		
	str_args  = None
	str_kargs = None		

	if (arr_args.__len__() != 0):
		str_args  = ','.join(arr_args)	

	if (arr_kargs.__len__() != 0):		
		str_kargs = ','.join(arr_kargs)

	ret = None

	try:
		if (str_args != None):
			if (str_kargs == None):
				ret = eval(f"function({str_args})")
			else:
				str_combined_args = str_args + ',' + str_kargs
				ret = eval(f"function({str_combined_args})")
		else:
			if (str_kargs != None):
				ret = eval(f"function({str_kargs})")
			else:
				ret = eval(f"function()")		
	except Exception as error:
		with open('py_errors.txt', 'a') as fd:
			fd.write(f'\n{format(error)}\n')
   
		print(error)
		sys.exit()

	if (ret != None):
		print(json.dumps(ret))




