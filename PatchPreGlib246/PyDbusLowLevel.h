/*
 * PyDbusLowLevel.h
 *
 *  Created on: Apr 21, 2017
 *      Author: Harry G. Coin, Quiet Fountain LLC
 */


#ifndef PYDBUSLOWLEVEL_H_
#define PYDBUSLOWLEVEL_H_

//#define Py_LIMITED_API


#include <Python.h>

#include "pygobject.h"

#include <gio/gio.h>

PyMODINIT_FUNC PyInit_PatchPreGlib246(void);
static PyObject * itsafact(PyObject *, PyObject *);
static PyObject * dbus_connection_register_object(PyObject *, PyObject *);
static PyObject * dbus_invocation_return_value(PyObject *, PyObject *);
static PyObject * dbus_invocation_return_dbus_error(PyObject *, PyObject *);

#endif
/* PYDBUSLOWLEVEL_H_ */

