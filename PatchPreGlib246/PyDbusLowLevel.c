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
#define HCPy_REFCNT(ob)           ((ob==NULL) ? -100 : ( ((PyObject*)(ob))->ob_refcnt) )


//static	PyTypeObject *pytype_GDBusMethodInvocation; //Because locking won't let the lookup query happen in a callback.
//static GQuark pygobject_instance_data_key;

//static inline PyGObjectData *
//pyg_object_peek_inst_data(GObject *obj)
//{
//    return ((PyGObjectData *)
//            g_object_get_qdata(obj, pygobject_instance_data_key));
//}



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

static PyObject* g_variant_to_pyobject (GVariant *variant)
{
    GValue value = { 0, };
    g_value_init (&value, G_TYPE_VARIANT);
    g_value_set_variant (&value, variant);
    return pyg_value_as_pyobject (&value, FALSE);
}



void cro_method_call(GDBusConnection *connection /*gobject*/, const gchar *sender,
		const gchar *object_path, const gchar *interface_name,
		const gchar *method_name, GVariant *parameters,
		GDBusMethodInvocation *invocation /*gobject*/, gpointer user_data) {

	PyObject *arglist=NULL,*py_parms=NULL,*py_invoke=NULL,*py_connection=NULL;
	struct dbus_connection_register_struct *reg_info=NULL;
	struct lock_detail lock;
	allow_python_calls(&lock);

#define gobj_info(x)  	/**/

/*PySys_WriteStderr("%d: c %ld p %ld i %ld a %ld %s floating %d ref %d\n", \
//	__LINE__, HCPy_REFCNT(py_connection), HCPy_REFCNT(py_parms), \
//	HCPy_REFCNT(py_invoke), HCPy_REFCNT(arglist),#x, \
//	g_object_is_floating(x), \
//	*(uint *)(((GTypeInstance *)x)+1))

*/

	gobj_info(connection);
	gobj_info(invocation);

	reg_info = (struct dbus_connection_register_struct *) user_data;

	py_parms = g_variant_to_pyobject(parameters);
	//py_parms = pyg_boxed_new(G_TYPE_VARIANT, g_variant_ref(parameters), FALSE, FALSE);

	//g_object_ref(connection);

	//py_connection = pyg_boxed_new(G_TYPE_DBUS_CONNECTION,connection, FALSE, FALSE);
	//py_invoke = pyg_boxed_new(G_TYPE_DBUS_METHOD_INVOCATION,invocation,FALSE,FALSE);

	py_connection = pygobject_new(G_OBJECT(connection));
	py_invoke = pygobject_new(G_OBJECT(invocation));

	gobj_info(connection);
	gobj_info(invocation);
	//puts(method_name);
	arglist = Py_BuildValue("NssssNN",
			py_connection,
			sender, object_path, interface_name, method_name,
			py_parms,
			py_invoke);
	if ((arglist==NULL) || (PyErr_Occurred()!=NULL)) {
		PyErr_PrintEx(0);
		exit(1);
	}

	//PySys_WriteStderr("%s\n",PyUnicode_AsUTF8(PyObject_Repr(arglist)));

	gobj_info(connection);
	gobj_info(invocation);

	PyObject_CallObject(reg_info->method_closure, arglist);

	//PySys_WriteStderr("end method call\n");
	gobj_info(connection);
	gobj_info(invocation);

	//PySys_WriteStderr("%d: %ld %ld %ld %ld\n",__LINE__,Py_REFCNT(py_connection),Py_REFCNT(py_parms),Py_REFCNT(py_invoke),Py_REFCNT(arglist));
	Py_DECREF(arglist);
	//PySys_WriteStderr("arglist free\n");
	Py_DECREF(py_parms);
	Py_DECREF(py_connection);
	Py_DECREF(py_invoke);
	//g_object_unref(connection);
	g_variant_unref(parameters);

	restore_previous_lock_state(&lock);

}

gboolean cro_set_property(GDBusConnection *connection, const gchar *sender,
		const gchar *object_path, const gchar *interface_name,
		const gchar *property_name, GVariant *value, GError **error,
		gpointer user_data) {
	PyObject *args,*kwargs,*p_value;
	gboolean ret=TRUE;
	struct dbus_connection_register_struct *reg_info;
	struct lock_detail lock;
	allow_python_calls(&lock);

	kwargs= PyDict_New();
	reg_info = (struct dbus_connection_register_struct *) user_data;
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
	Py_DECREF(args);
	Py_DECREF(kwargs);
	restore_previous_lock_state(&lock);
	return ret;
}

GVariant * cro_get_property(GDBusConnection *connection, const gchar *sender,
		const gchar *object_path, const gchar *interface_name,
		const gchar *property_name, GError **error, gpointer user_data) {
	PyObject *args,*kwargs,*error_info;
	PyObject *result;
	GVariant *ret;

	struct dbus_connection_register_struct *reg_info;
	struct lock_detail lock;
	allow_python_calls(&lock);


	reg_info = (struct dbus_connection_register_struct *) user_data;


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
		//puts(g_variant_get_type_string(ret));
	}
	Py_DECREF(args);
	Py_DECREF(kwargs);
	//Py_DECREF(result);

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
	PyObject *g_inv;
	PyObject *g_parameters;

	PyArg_ParseTuple(args, "OO", &g_inv,&g_parameters);

	Py_BEGIN_ALLOW_THREADS

	g_dbus_method_invocation_return_value(pyg_pointer_get(g_inv,GDBusMethodInvocation),
										  pyg_pointer_get(g_parameters,GVariant));
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

