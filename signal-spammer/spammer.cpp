#include <iostream>
#include <gio/gio.h>
#include <stdlib.h>

#ifdef G_OS_UNIX
#include <gio/gunixfdlist.h>
/* For STDOUT_FILENO */
#include <unistd.h>
#endif

/* ---------------------------------------------------------------------------------------------------- */

static GDBusNodeInfo *introspection_data = NULL;

/* Introspection data for the service we are exporting */
static const gchar introspection_xml[] =
  "<node>"
  "  <interface name='net.lew21.pydbus.SignalSpammer'>"
  "    <signal name='Wow'>"
  "      <arg type='d' name='first_arg'/>"
  "    </signal>"
  "  </interface>"
  "</node>";

/* ---------------------------------------------------------------------------------------------------- */

static void
handle_method_call (GDBusConnection       *connection,
					const gchar           *sender,
					const gchar           *object_path,
					const gchar           *interface_name,
					const gchar           *method_name,
					GVariant              *parameters,
					GDBusMethodInvocation *invocation,
					gpointer               user_data)
{}

static GVariant *
handle_get_property(GDBusConnection  *connection,
					const gchar      *sender,
					const gchar      *object_path,
					const gchar      *interface_name,
					const gchar      *property_name,
					GError          **error,
					gpointer          user_data)
{
	GVariant *ret;
	ret = NULL;
	return ret;
}

static gboolean
handle_set_property(GDBusConnection  *connection,
					const gchar      *sender,
					const gchar      *object_path,
					const gchar      *interface_name,
					const gchar      *property_name,
					GVariant         *value,
					GError          **error,
					gpointer          user_data)
{
	return *error == NULL;
}

static const GDBusInterfaceVTable interface_vtable =
{
	handle_method_call,
	handle_get_property,
	handle_set_property
};

void emit_signal(GDBusConnection* connection)
{
	auto local_error = (GError*)nullptr;
	g_dbus_connection_emit_signal(connection,
		NULL,
		"/net/lew21/pydbus/SignalSpammer",
		"net.lew21.pydbus.SignalSpammer",
		"Wow",
		g_variant_new("(d)", (gdouble)5),
		&local_error);
	g_assert_no_error(local_error);
}

static gboolean
on_timeout_cb(gpointer user_data)
{
	emit_signal(G_DBUS_CONNECTION(user_data));
	return true;
}
/* ---------------------------------------------------------------------------------------------------- */

static void on_bus_acquired(GDBusConnection* connection, const gchar* name, gpointer user_data)
{
	auto registration_id = g_dbus_connection_register_object(connection,
		"/net/lew21/pydbus/SignalSpammer",
		introspection_data->interfaces[0],
		&interface_vtable,
		NULL,  /* user_data */
		NULL,  /* user_data_free_func */
		NULL); /* GError** */
	g_assert(registration_id > 0);

	g_timeout_add_seconds(2, on_timeout_cb, connection);
}

static void on_name_acquired(GDBusConnection* connection, const gchar* name, gpointer user_data)
{}

static void on_name_lost(GDBusConnection* connection, const gchar* name, gpointer user_data)
{
	exit(1);
}

int main(int argc, char** argv)
{
	guint owner_id;
	GMainLoop *loop;

	/* We are lazy here - we don't want to manually provide
	* the introspection data structures - so we just build
	* them from XML.
	*/
	introspection_data = g_dbus_node_info_new_for_xml(introspection_xml, NULL);
	g_assert(introspection_data != NULL);

	owner_id = g_bus_own_name(G_BUS_TYPE_SESSION, "net.lew21.pydbus.SignalSpammer", G_BUS_NAME_OWNER_FLAGS_NONE, on_bus_acquired, on_name_acquired, on_name_lost, NULL, NULL);

	loop = g_main_loop_new(NULL, FALSE);
	g_main_loop_run(loop);

	g_bus_unown_name(owner_id);

	g_dbus_node_info_unref(introspection_data);

	return 0;
}
