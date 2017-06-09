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

static	PyTypeObject *pytype_GDBusMethodInvocation; //Because locking won't let the lookup query happen in a callback.
static GQuark pygobject_instance_data_key;

static inline PyGObjectData *
pyg_object_peek_inst_data(GObject *obj)
{
    return ((PyGObjectData *)
            g_object_get_qdata(obj, pygobject_instance_data_key));
}



static PyMethodDef methodlist[] = {
		{ "itsafact", itsafact,
		METH_VARARGS, "Interface test: return a factorial" },
		{"dbus_connection_register_object",	dbus_connection_register_object,
		METH_VARARGS, "Workaround python to GLib pre v2.46 bug." }, { NULL, NULL, 0, NULL } };

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

static GVariant *gvnoop;
static GObject *gnone;
static GQuark PyDbusQuark;

PyMODINIT_FUNC PyInit_PatchPreGlib246(void) {
		//PyEval_InitThreads();
		pygobject_init(-1, -1, -1);
		gvnoop = g_variant_new("i",0);
		gnone = g_object_new(G_TYPE_NONE,0);
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

static void reg_info_free(void *p) {
	struct dbus_connection_register_struct *reg_info =
			(struct dbus_connection_register_struct *) p;
	Py_DECREF(reg_info->connection);
	Py_DECREF(reg_info->interface);
	Py_DECREF(reg_info->method_closure);
	Py_DECREF(reg_info->get_prop_closure);
	Py_DECREF(reg_info->set_prop_closure);
	PyMem_Free(reg_info->path);
	PyMem_Free(p);
}



void cro_method_call(GDBusConnection *connection, const gchar *sender,
		const gchar *object_path, const gchar *interface_name,
		const gchar *method_name, GVariant *parameters,
		GDBusMethodInvocation *invocation, gpointer user_data) {

	PyObject *arglist,*py_parms,*py_invoke,*py_connection;
	struct dbus_connection_register_struct *reg_info;
	PyThreadState *PyTState;
	
	reg_info = (struct dbus_connection_register_struct *) user_data;

	PyTState = PyGILState_GetThisThreadState();
	PyEval_RestoreThread(PyTState);

	py_connection = pygobject_new(G_OBJECT(connection));
	py_parms = pyg_boxed_new(G_TYPE_VARIANT, g_variant_ref(parameters), FALSE, FALSE);
	py_invoke = pygobject_new(G_OBJECT(invocation));

	arglist = Py_BuildValue("OssssOO",
			py_connection,
			sender, object_path, interface_name, method_name,
			py_parms,
			py_invoke);

	PyObject_CallObject(reg_info->method_closure, arglist);
	Py_DECREF(arglist);

	PyEval_SaveThread();
}

gboolean cro_set_property(GDBusConnection *connection, const gchar *sender,
		const gchar *object_path, const gchar *interface_name,
		const gchar *property_name, GVariant *value, GError **error,
		gpointer user_data) {
	PyObject *args,*kwargs;
	gboolean ret=TRUE;
	struct dbus_connection_register_struct *reg_info;
	kwargs= PyDict_New();
	reg_info = (struct dbus_connection_register_struct *) user_data;
	args = Py_BuildValue("ssv",interface_name,property_name,value);
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
	return ret;
}

GVariant * cro_get_property(GDBusConnection *connection, const gchar *sender,
		const gchar *object_path, const gchar *interface_name,
		const gchar *property_name, GError **error, gpointer user_data) {
	PyObject *args,*kwargs;
	GVariant *ret;
	struct dbus_connection_register_struct *reg_info;
	reg_info = (struct dbus_connection_register_struct *) user_data;
	args = Py_BuildValue("ss",interface_name,property_name);
	kwargs= PyDict_New();
	ret = (GVariant *) PyObject_Call(reg_info->get_prop_closure,args,kwargs);
	if (PyDict_Size(kwargs)>0) {
		g_set_error_literal(error,PyDbusQuark,1,PyByteArray_AsString(PyDict_GetItemString(kwargs,"exception")));
		ret=NULL;
	}
	Py_DECREF(args);
	Py_DECREF(kwargs);
	return ret;
}

#ifdef Bad_Ideas_Whose_Time_Will_Never_Come
GVariant * cro_get_property(GDBusConnection *connection, const gchar *sender,
		const gchar *object_path, const gchar *interface_name,
		const gchar *property_name, GError **error, gpointer user_data) {
	//PyObject *arglist;
	//PyGObject *result;
	//struct dbus_connection_register_struct *reg_info;
	//reg_info = (struct dbus_connection_register_struct *) user_data;

	//arglist = Py_BuildValue("Ossss",
	//pygobject_new(G_OBJECT(connection)), sender, object_path, interface_name,
	//		property_name);
	//result = (PyGObject *) PyObject_CallObject(reg_info->get_prop_closure,
	//		arglist);
	//Py_DECREF(arglist);
	//if (pyg_gerror_exception_check(error) != 0)
	//	return NULL;
	//if (result == NULL) {
	//	return NULL;
	//}
	//return (GVariant *) result->obj;

	PyObject *arglist,*py_connection;
	struct dbus_connection_register_struct *reg_info;
	PyThreadState *PyTState;
	GVariant *ret; PyObject *pyret;

	reg_info = (struct dbus_connection_register_struct *) user_data;

	PyTState = PyGILState_GetThisThreadState();
	PyEval_RestoreThread(PyTState);

	py_connection = pygobject_new(G_OBJECT(connection));
	//py_parms = pyg_boxed_new(G_TYPE_VARIANT, g_variant_ref(parameters), FALSE, FALSE);
	//py_invoke = pygobject_new(G_OBJECT(invocation));

	arglist = Py_BuildValue("Ossss",
			py_connection,
			sender, object_path, interface_name, property_name);

	pyret = PyObject_CallObject(reg_info->get_prop_closure, arglist);
	PyObject_Print(pyret,stdout,0);
	printf(" -- result\n");

	if ((pyg_gerror_exception_check(error) != 0) || (pyret == NULL)) {
		ret= NULL;
	} else {
		ret = pyg_boxed_get(pyret,GVariant);
	}
	Py_DECREF(arglist);

	PyEval_SaveThread();
	return ret;
}



gboolean cro_set_property(GDBusConnection *connection, const gchar *sender,
		const gchar *object_path, const gchar *interface_name,
		const gchar *property_name, GVariant *value, GError **error,
		gpointer user_data) {
	//PyObject *arglist;
	//struct dbus_connection_register_struct *reg_info;
	//
	//reg_info = (struct dbus_connection_register_struct *) user_data;
	//
	//arglist = Py_BuildValue("OssssO",
	//pygobject_new(G_OBJECT(connection)), sender, object_path, interface_name,
	//		property_name, value);
	//PyObject_CallObject(reg_info->set_prop_closure, arglist);
	//Py_DECREF(arglist);
	//

	PyObject *arglist,*py_parms,*py_connection;
	struct dbus_connection_register_struct *reg_info;
	PyThreadState *PyTState;
	gboolean ret;

	reg_info = (struct dbus_connection_register_struct *) user_data;

	PyTState = PyGILState_GetThisThreadState();
	PyEval_RestoreThread(PyTState);

	py_connection = pygobject_new(G_OBJECT(connection));
	py_parms = pyg_boxed_new(G_TYPE_VARIANT, g_variant_ref(value), FALSE, FALSE);
	//py_invoke = pygobject_new(G_OBJECT(invocation));

	arglist = Py_BuildValue("OssssO",
			py_connection,
			sender, object_path, interface_name, property_name,
			py_parms);

	PyObject_CallObject(reg_info->set_prop_closure, arglist);
	ret = pyg_gerror_exception_check(error);
	Py_DECREF(arglist);

	PyEval_SaveThread();
	return ret;

}

#endif

PyObject * dbus_connection_register_object(PyObject *self, PyObject *args) {
	int i;
	const char *s;
	struct dbus_connection_register_struct *reg_info;
	GObject *giomm_connection;
	GObject *giomm_interface;
	GDBusConnection *connection;
	GDBusInterfaceInfo *interface;
	GType gdbusinv;
	reg_info = (struct dbus_connection_register_struct *) PyMem_Malloc(
			sizeof(struct dbus_connection_register_struct));
	memset((void *) reg_info, 0, sizeof(*reg_info)); // old age teaches many things.
	PyArg_ParseTuple(args, "OsOOOO", &reg_info->connection, &s,
			&reg_info->interface, &reg_info->method_closure,
			&reg_info->get_prop_closure, &reg_info->set_prop_closure);
	reg_info->path = (char *) PyMem_Malloc(strlen(s) + 1);
	strcpy(reg_info->path, s);
	reg_info->vtable.method_call = cro_method_call;
	reg_info->vtable.get_property = cro_get_property;
	reg_info->vtable.set_property = cro_set_property;
	Py_INCREF(reg_info->connection);
	Py_INCREF(reg_info->interface);
	Py_INCREF(reg_info->method_closure);
	Py_INCREF(reg_info->get_prop_closure);
	Py_INCREF(reg_info->set_prop_closure);
	giomm_connection = reg_info->connection->obj;
	giomm_interface = reg_info->interface->obj;
	connection = (GDBusConnection *) giomm_connection;
	interface = (GDBusInterfaceInfo *) giomm_interface;
	gdbusinv = G_TYPE_DBUS_METHOD_INVOCATION;
	pytype_GDBusMethodInvocation = 	pygobject_lookup_class(gdbusinv);
	pygobject_instance_data_key = g_quark_from_static_string("PyGObject::instance-data");
	i = g_dbus_connection_register_object(connection, reg_info->path, interface,
			&reg_info->vtable, reg_info, reg_info_free, &reg_info->error);

	return PyLong_FromLong(i);
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

