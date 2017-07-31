/*
 PyDbusLowLevel.c
 *
 *  Created on: Apr 21, 2017
 *      Author: Harry G. Coin, Quiet Fountain LLC
 *      Copyright: Lesser GPL.
 *
 *      Low level C and C++ code necessary to support pydbus functions.
 *
 *      Python's introspection Gio glue did not properly implement
 *      dbus_connection_register_object in versions prior to at least 2.46
 *      This module provides proper operation so pydbus can support all
 *      gio libraries.
 *      See:  https://bugzilla.gnome.org/show_bug.cgi?id=656325
 */

#include "PyDbusLowLevel.h" 

//There is psuedo ugliness here access private glib structures.
//It is acceptable only because this code will only be called
//when using old versions of the libraries, and not versions
//post glib 2.46 or so.

struct HGVariant

{
  int *type_info;
  gsize size;

  union
  {
    struct
    {
      GBytes *bytes;
      gconstpointer data;
    } serialised;

    struct
    {
      GVariant **children;
      gsize n_children;
    } tree;
  } contents;

  gint state;
  gint ref_count;
};

//struct  HGObject
//{
// GTypeInstance  g_type_instance;
//
  /*< private >*/
//  volatile guint ref_count;
//  GData         *qdata;
//};






#define HCGVariant_REFCNT(ob)	  ((ob==NULL) ? (uint)-100 : *(((uint *)(        ((struct HGVariant *) ob)        +1))-1))
#define HCGObject_REFCNT(ob)	  ((ob==NULL) ? (uint)-100 : *((uint *)(((GTypeInstance *)ob)+1)))


long HCPy_REFCNT(PyObject *ob){
	long rc=0,vr=0;
	if (ob==NULL) return -100;
	rc= ob->ob_refcnt;
	if (pyg_type_from_object(ob)==G_TYPE_VARIANT) {
		vr = HCGVariant_REFCNT(pyg_pointer_get(ob,GVariant));
		if (vr!=rc) return -(rc+ 1000*(100+vr));
		return rc+1000*(100+vr);
	}
	return rc;

}

int HCGError_info(GError **e) {
	GError *e1;
	if (e==NULL) return -100;
	e1 = *e;
	if (e1==NULL) return -101;
	return e1->code;
}

static PyMethodDef methodlist[] = {
		{ "itsafact", itsafact,
		METH_VARARGS, "Interface test: return a factorial" },

		{"compat_dbus_connection_register_object",	dbus_connection_register_object,
		METH_VARARGS, "Workaround python to GLib pre v2.46 bug." },

		{"compat_dbus_invocation_return_value",	dbus_invocation_return_value,
		METH_VARARGS, "Workaround python to GLib pre v2.46 bug." },

		{"compat_dbus_invocation_return_dbus_error",	dbus_invocation_return_dbus_error,
		METH_VARARGS, "Workaround python to GLib pre v2.46 bug." },

		{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef PatchPreGlib246module = {
		PyModuleDef_HEAD_INIT, "PatchPreGlib246",
#if WORDSIZE == 64
#ifdef PYDBUSDEBUGGING
		"C++ and C helper functions for PyDBus 64 bit with debug info", -1, methodlist };
#else
	"C++ and C helper functions for PyDBus 64 bit", -1,	methodlist};
#endif
#else
	"C++ and C helper functions for PyDBus 32 bit", -1,	methodlist};
#endif

//static GVariant *gvnoop;
//static GObject *gnone;
static GQuark PyDbusQuark;

PyMODINIT_FUNC PyInit_PatchPreGlib246(void) {
		//PyEval_InitThreads();
		pygobject_init(-1, -1, -1);

		//gvnoop = g_variant_new("i",0);
		//gnone = g_object_new(G_TYPE_OBJECT,NULL);
		PyDbusQuark = g_quark_from_static_string("PatchPreGlib246");

		return PyModule_Create ( &PatchPreGlib246module);

}


struct dbus_connection_register_struct {
	char * path;
	PyGObject * connection;
	PyGObject * interface;
	PyObject * method_closure, *get_prop_closure, *set_prop_closure;
	GDBusInterfaceVTable vtable;
	GError *error;
	GVariant *get_result;
};

static void reg_info_free(gpointer p) {
	struct dbus_connection_register_struct *reg_info =
			(struct dbus_connection_register_struct *) p;
	Py_XDECREF(reg_info->connection);
	Py_XDECREF(reg_info->interface);
	Py_XDECREF(reg_info->method_closure);
	Py_XDECREF(reg_info->get_prop_closure);
	Py_XDECREF(reg_info->set_prop_closure);
	g_free(p);
}

struct lock_detail {
	PyGILState_STATE GIL_state;
};

static void allow_python_calls(struct lock_detail *ld){
	ld->GIL_state=PyGILState_Ensure();
}

static void restore_previous_lock_state(struct lock_detail *ld){
	PyGILState_Release(ld->GIL_state);
}

//void align_refs_py_gvariant(PyObject *p,GVariant *v){
//    p->ob_refcnt = HCGVariant_REFCNT(v);
//}


static PyObject* g_variant_to_pyobject (GVariant *variant)
{
    GValue value;
	PyObject *ret=NULL;
    memset(&value,0,sizeof(value));
    g_value_init (&value, G_TYPE_VARIANT);
    //PySys_WriteStderr("in g2py gvar %d pyret %ld\n",HCGVariant_REFCNT(variant),HCPy_REFCNT(ret));
    g_value_set_variant (&value, variant);  //glib reference value+1
    ret=pyg_value_as_pyobject (&value, FALSE); //glib reference to value+2 pyref ret=1
    //g_variant_unref(variant); //glib reference value+1
    //g_variant_unref(variant); //glib reference value
    //align_refs_py_gvariant(ret,variant);
    //PySys_WriteStderr("out g2py gvar %d pyret %ld\n",HCGVariant_REFCNT(variant),HCPy_REFCNT(ret));
    return ret;
}




void cro_method_call(GDBusConnection *connection /*gobject*/, const gchar *sender,
		const gchar *object_path, const gchar *interface_name,
		const gchar *method_name, GVariant *parameters,
		GDBusMethodInvocation *invocation /*gobject*/, gpointer user_data) {

	PyObject *arglist=NULL,*py_parms=NULL,*py_invoke=NULL,*py_connection=NULL;
	struct dbus_connection_register_struct *reg_info=NULL;
	struct lock_detail lock;
	allow_python_calls(&lock);

	reg_info = (struct dbus_connection_register_struct *) user_data;

	//PySys_WriteStderr("a py_invoke %ld, py_conn %ld py_parms %ld arglist %ld, parms %d inv %d conn %d\n",
	//		HCPy_REFCNT(py_invoke), HCPy_REFCNT(py_connection),HCPy_REFCNT(py_parms),HCPy_REFCNT(arglist),
	//		HCGVariant_REFCNT(parameters),
	//		HCGObject_REFCNT(invocation),
	//		HCGObject_REFCNT(connection)
	//		);

	py_parms = g_variant_to_pyobject(parameters);

	py_connection = pygobject_new(G_OBJECT(connection));
	py_invoke = pygobject_new(G_OBJECT(invocation));

	//PySys_WriteStderr("b py_invoke %ld, py_conn %ld py_parms %ld arglist %ld, parms %d inv %d conn %d\n",
	//		HCPy_REFCNT(py_invoke), HCPy_REFCNT(py_connection),HCPy_REFCNT(py_parms),HCPy_REFCNT(arglist),
	//		HCGVariant_REFCNT(parameters),
	//		HCGObject_REFCNT(invocation),
	//		HCGObject_REFCNT(connection)
	//		);

	arglist = Py_BuildValue("NssssNN",
			py_connection,
			sender, object_path, interface_name, method_name,
			py_parms,
			py_invoke);

	if ((arglist==NULL) || (PyErr_Occurred()!=NULL)) {
		PyErr_PrintEx(0);
		exit(1);
	}

	//PySys_WriteStderr("c py_invoke %ld, py_conn %ld py_parms %ld arglist %ld, parms %d inv %d conn %d\n",
	//		HCPy_REFCNT(py_invoke), HCPy_REFCNT(py_connection),HCPy_REFCNT(py_parms),HCPy_REFCNT(arglist),
	//		HCGVariant_REFCNT(parameters),
	//		HCGObject_REFCNT(invocation),
	//		HCGObject_REFCNT(connection)
	//		);

	PyObject_CallObject(reg_info->method_closure, arglist);

	//PySys_WriteStderr("d py_invoke %ld, py_conn %ld py_parms %ld arglist %ld, parms %d inv %d conn %d\n",
	//		HCPy_REFCNT(py_invoke), HCPy_REFCNT(py_connection),HCPy_REFCNT(py_parms),HCPy_REFCNT(arglist),
	//		HCGVariant_REFCNT(parameters),
	//		HCGObject_REFCNT(invocation),
	//		HCGObject_REFCNT(connection)
	//		);

	Py_DECREF(arglist);

	//PySys_WriteStderr("e py_invoke %ld, py_conn %ld py_parms %ld arglist %ld, parms %d inv %d conn %d\n",
	//		HCPy_REFCNT(py_invoke), HCPy_REFCNT(py_connection),HCPy_REFCNT(py_parms),HCPy_REFCNT(arglist),
	//		HCGVariant_REFCNT(parameters),
	//		HCGObject_REFCNT(invocation),
	//		HCGObject_REFCNT(connection)
	//		);

	restore_previous_lock_state(&lock);

}




gboolean cro_set_property(GDBusConnection *connection, const gchar *sender,
		const gchar *object_path, const gchar *interface_name,
		const gchar *property_name, GVariant *value, GError **error,
		gpointer user_data) {
	PyObject *args=NULL,*kwargs=NULL,*p_value=NULL;
	gboolean ret=TRUE;
	struct dbus_connection_register_struct *reg_info;
	struct lock_detail lock;
	allow_python_calls(&lock);

	kwargs= PyDict_New();
	reg_info = (struct dbus_connection_register_struct *) user_data;
	//PySys_WriteStderr("s1 kwargs %ld, p_value %ld, value %d conn %d error %d args %ld\n",
	//		HCPy_REFCNT(kwargs),HCPy_REFCNT(p_value),HCGVariant_REFCNT(value),
	//		HCGObject_REFCNT(connection),HCGError_info(error),
	//		HCPy_REFCNT(args));
	p_value =g_variant_to_pyobject(value);
	args = Py_BuildValue("ssO",interface_name,property_name,p_value);
	if (args==NULL) {
		PyErr_PrintEx(0);
		exit(1);
	}
	PyObject_Call(reg_info->set_prop_closure,args,kwargs);
	if (PyDict_Size(kwargs)>0) {
		PyObject *p_errv;
		const char *errv;
		p_errv=PyDict_GetItemString(kwargs,"exception");
		errv=PyByteArray_AsString(p_errv);
		g_set_error_literal(error,PyDbusQuark,1,errv);
		ret = 0;
	}
	g_variant_ref(value);
	Py_DECREF(kwargs);
	Py_DECREF(p_value);
	Py_DECREF(args);
	//PySys_WriteStderr("s2 kwargs %ld, p_value %ld, value %d conn %d error %d args %ld\n",
	//		HCPy_REFCNT(kwargs),HCPy_REFCNT(p_value),HCGVariant_REFCNT(value),
	//		HCGObject_REFCNT(connection),HCGError_info(error),
	//		HCPy_REFCNT(args));
	restore_previous_lock_state(&lock);
	return ret;
}




GVariant * cro_get_property(GDBusConnection *connection, const gchar *sender,
		const gchar *object_path, const gchar *interface_name,
		const gchar *property_name, GError **error, gpointer user_data) {
	PyObject *args=NULL,*kwargs=NULL,*error_info=NULL;
	PyObject *result=NULL;
	GVariant *ret=NULL;

	struct dbus_connection_register_struct *reg_info;
	struct lock_detail lock;
	allow_python_calls(&lock);


	reg_info = (struct dbus_connection_register_struct *) user_data;

	//PySys_WriteStderr("g1 kwargs %ld, conn %d error %d args %ld err_info %ld result %ld ret %d\n",
	//		HCPy_REFCNT(kwargs),
	//		HCGObject_REFCNT(connection),HCGError_info(error),HCPy_REFCNT(args),
	//		HCPy_REFCNT(error_info),HCPy_REFCNT(result),HCGVariant_REFCNT(ret));
	args = Py_BuildValue("ss",interface_name,property_name);
	if (args==NULL) {
		PyErr_PrintEx(0);
		exit(1);
	}
	kwargs= PyDict_New();
	result = PyObject_Call(reg_info->get_prop_closure,args,kwargs);
	error_info = PyDict_GetItemString(kwargs,"exception");
	if (error_info!=NULL) {
		g_set_error_literal(error,PyDbusQuark,1,PyByteArray_AsString(error_info));
		ret=NULL;
	} else {
		ret = pyg_pointer_get(result,GVariant);
	}
	Py_DECREF(args);
	Py_DECREF(kwargs);
	g_variant_ref(ret);
	Py_DECREF(result);
	//PySys_WriteStderr("g2 kwargs %ld, conn %d error %d args %ld err_info %ld result %ld ret %d\n",
	//		HCPy_REFCNT(kwargs),
	//		HCGObject_REFCNT(connection),HCGError_info(error),HCPy_REFCNT(args),
	//		HCPy_REFCNT(error_info),HCPy_REFCNT(result),HCGVariant_REFCNT(ret));


	restore_previous_lock_state(&lock);

	return ret;
}



PyObject * dbus_connection_register_object(PyObject *self, PyObject *args) {
	guint i;
	struct dbus_connection_register_struct *reg_info;
	PyObject *ret_long;
	GDBusConnection *connection;
	GDBusInterfaceInfo *interface;

	reg_info = g_new0(struct dbus_connection_register_struct,1);

	reg_info->vtable.method_call  = cro_method_call;
	reg_info->vtable.get_property = cro_get_property;
	reg_info->vtable.set_property = cro_set_property;

	if (!PyArg_ParseTuple(args, "OsOOOO", &reg_info->connection,
		&reg_info->path,
		&reg_info->interface,
		&reg_info->method_closure, &reg_info->get_prop_closure, &reg_info->set_prop_closure)) {
		PyErr_PrintEx(0);
		exit(1);
	}
	Py_XINCREF(reg_info->connection);
	Py_XINCREF(reg_info->interface);
	Py_XINCREF(reg_info->method_closure);
	Py_XINCREF(reg_info->get_prop_closure);
	Py_XINCREF(reg_info->set_prop_closure);

	connection = pyg_pointer_get(reg_info->connection,GDBusConnection);
	interface  = pyg_pointer_get(reg_info->interface, GDBusInterfaceInfo);

	//Py_BEGIN_ALLOW_THREADS
	i = g_dbus_connection_register_object(connection, reg_info->path, interface,
			&reg_info->vtable, reg_info, reg_info_free, &reg_info->error);
	//Py_END_ALLOW_THREADS

	ret_long = PyLong_FromLong(i);
	return ret_long;
}


PyObject * dbus_invocation_return_value(PyObject *self, PyObject *args) {
	PyObject *g_inv,*g_parms;
	GVariant *g_parameters;

	g_inv=PyTuple_GET_ITEM(args,0);
	g_parms = PyTuple_GetItem(args,1);
	if (g_parms==Py_None) {
		g_parameters = NULL;
	} else {
		g_parameters=pyg_pointer_get(g_parms,GVariant);
	}
	Py_BEGIN_ALLOW_THREADS

	g_dbus_method_invocation_return_value(pyg_pointer_get(g_inv,GDBusMethodInvocation),
										  g_parameters);
	Py_END_ALLOW_THREADS

	Py_RETURN_NONE;
}

PyObject * dbus_invocation_return_dbus_error(PyObject *self, PyObject *args) {
	PyObject *g_inv;
	const gchar *g_errname,*g_errmsg;

	PyArg_ParseTuple(args, "Oss", &g_inv,&g_errname,&g_errmsg);

	Py_BEGIN_ALLOW_THREADS

	g_dbus_method_invocation_return_dbus_error(pyg_pointer_get(g_inv,GDBusMethodInvocation),
										  g_errname,g_errmsg);
	Py_END_ALLOW_THREADS

	Py_RETURN_NONE;
}

/* Compute factorial of n */
PyObject * itsafact(PyObject *self, PyObject *args) {
	long n;
	n = 0;
	PyArg_ParseTuple(args, "l", &n);
	PySys_WriteStdout("%ld\n", n);
	if (n <= 1) {
		return PyLong_FromLong(1);
	} else {
		return PyLong_FromLong(
				n
						* PyLong_AsLong(
								itsafact(self,
										Py_BuildValue("(l)", n - 1))));
	}
}

