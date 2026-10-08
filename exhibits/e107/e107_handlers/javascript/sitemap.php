
var ejs_func_todo='view';

function ejs_expandall(ejs_cl_name,ejs_func_todo,ejs_cl_name2){

	tot_object = document.getElementsByTagName('p').length;

	for(i=0;i<tot_object;i++){

		sp = document.getElementsByTagName('span').item(i);

		p = document.getElementsByTagName('p').item(i);

		if(p.id!=''){

			if(p.className==ejs_cl_name){

				if(ejs_func_todo=='view'){

					if(p!=0)p.style.display='block';

				}else if(ejs_func_todo=='hide'){

					if(p!=0)p.style.display='none';

				}

			}

		}else if(sp){

			if(sp.className==ejs_cl_name || (ejs_cl_name2!='undefined' && sp.className==ejs_cl_name2)){

				if(ejs_func_todo=='view'){

					if(sp!=0)sp.style.display='block';

				}else if(ejs_func_todo=='hide'){

					if(sp!=0)sp.style.display='none';

				}

			}

		}

	}

	if(ejs_func_todo=='hide'){ejs_func_todo='view';}else{ejs_func_todo='hide';}

	ejs_expandpics('icoexp',ejs_func_todo2,'SM_ICO_URL','SM_ICO_URL2');

	return ejs_func_todo;

}



var ejs_func_todo2='hide';

function ejs_expandpics(ejs_cl_name,ejs_func_todo2,src1,src2){

	tot_object2 = document.getElementsByTagName('img').length;


	for(i=0;i<tot_object2;i++){

		im = document.getElementsByTagName('img').item(i);

		if(im.className==ejs_cl_name){

				if(ejs_func_todo2=='view'){

					im.src=src1;

				}else if(ejs_func_todo2=='hide'){

					im.src=src2;

				}

		}

	}

	if(ejs_func_todo2=='hide'){ejs_func_todo2='view';}else{ejs_func_todo2='hide';}

	return ejs_func_todo2;

}

