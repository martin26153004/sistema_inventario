# ======================================================
# CLASE InventarioTienda
# ======================================================


class InventarioTienda:
    """Gestiona el inventario de productos de una tienda."""

    def __init__(self, nombre_tienda):
        """
        Inicializa una tienda con un inventario vacío.

        Args:
            nombre_tienda (str): Nombre de la tienda.
        """
        self.nombre_tienda = nombre_tienda
        self._productos = []

    def agregar_producto(self, nombre, precio, cantidad):
        """
        Agrega un producto al inventario.

        Si el producto ya existe, se suma la cantidad nueva
        a la cantidad existente.
        """
        nombre = nombre.strip()

        if not nombre:
            raise ValueError(
                "El nombre del producto no puede estar vacío"
            )

        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")

        # Buscar si el producto ya existe.
        for producto in self._productos:
            if producto["nombre"].lower() == nombre.lower():
                producto["cantidad"] += cantidad
                return

        # Si no existe, se agrega como un producto nuevo.
        nuevo_producto = {
            "nombre": nombre,
            "precio": precio,
            "cantidad": cantidad
        }

        self._productos.append(nuevo_producto)

    def vender_producto(self, nombre, cantidad):
        """
        Reduce la cantidad disponible de un producto.

        Raises:
            ValueError: Si la cantidad es inválida, el producto
            no existe o no hay suficiente stock.
        """
        nombre = nombre.strip()

        if not nombre:
            raise ValueError(
                "El nombre del producto no puede estar vacío"
            )

        if cantidad <= 0:
            raise ValueError(
                "La cantidad a vender debe ser mayor a 0"
            )

        for producto in self._productos:
            if producto["nombre"].lower() == nombre.lower():

                if cantidad > producto["cantidad"]:
                    raise ValueError(
                        f"No hay suficiente stock de "
                        f"'{producto['nombre']}'. "
                        f"Disponible: {producto['cantidad']}"
                    )

                producto["cantidad"] -= cantidad
                return

        raise ValueError(
            f"El producto '{nombre}' no se encuentra en el inventario"
        )

    def mostrar_inventario(self):
        """Muestra todos los productos registrados."""
        if not self._productos:
            print("\nEl inventario está vacío.")
            return

        print("\n" + "=" * 60)
        print(f"INVENTARIO DE {self.nombre_tienda.upper()}")
        print("=" * 60)
        print(f"{'Producto':<25}{'Precio':>15}{'Cantidad':>15}")
        print("-" * 60)

        for producto in self._productos:
            print(
                f"{producto['nombre']:<25}"
                f"${producto['precio']:>14.2f}"
                f"{producto['cantidad']:>15}"
            )

        print("=" * 60)

    def producto_mas_caro(self):
        """
        Devuelve el nombre y precio del producto más caro.

        Returns:
            tuple: Nombre y precio del producto más caro.
            None: Si el inventario está vacío.
        """
        if not self._productos:
            return None

        producto = max(
            self._productos,
            key=lambda elemento: elemento["precio"]
        )

        return producto["nombre"], producto["precio"]

    @property
    def total_productos(self):
        """
        Devuelve el número de productos diferentes.

        No suma las cantidades de los productos.
        """
        return len(self._productos)

    @property
    def valor_total_inventario(self):
        """Calcula el valor monetario total del inventario."""
        return sum(
            producto["precio"] * producto["cantidad"]
            for producto in self._productos
        )

    @property
    def productos_bajo_stock(self):
        """Devuelve los productos cuya cantidad es menor o igual a 5."""
        return [
            producto
            for producto in self._productos
            if producto["cantidad"] <= 5
        ]

    def ejecutar(self):
        """Ejecuta el menú interactivo del sistema."""
        while True:
            print("\n" + "=" * 50)
            print(f"SISTEMA DE INVENTARIO: {self.nombre_tienda}")
            print("=" * 50)
            print("1. Agregar producto")
            print("2. Vender producto")
            print("3. Mostrar inventario")
            print("4. Producto más caro")
            print("5. Mostrar estadísticas")
            print("6. Productos con bajo stock")
            print("7. Salir")
            print("=" * 50)

            opcion = input("Selecciona una opción: ").strip()

            try:
                if opcion == "1":
                    self._opcion_agregar_producto()

                elif opcion == "2":
                    self._opcion_vender_producto()

                elif opcion == "3":
                    self.mostrar_inventario()

                elif opcion == "4":
                    self._opcion_producto_mas_caro()

                elif opcion == "5":
                    self._opcion_mostrar_estadisticas()

                elif opcion == "6":
                    self._opcion_productos_bajo_stock()

                elif opcion == "7":
                    print(
                        f"\nGracias por utilizar el sistema de "
                        f"{self.nombre_tienda}."
                    )
                    print("Programa finalizado.")
                    break

                else:
                    print(
                        "\nOpción no válida. Selecciona una opción "
                        "del 1 al 7."
                    )

            except ValueError as error:
                print(f"\nError: {error}")

    def _opcion_agregar_producto(self):
        """Solicita los datos necesarios para agregar un producto."""
        print("\n--- Agregar producto ---")

        nombre = input("Nombre del producto: ").strip()

        if not nombre:
            raise ValueError(
                "El nombre del producto no puede estar vacío"
            )

        try:
            precio = float(input("Precio del producto: $"))
        except ValueError:
            raise ValueError(
                "El precio debe ser un número válido"
            )

        try:
            cantidad = int(input("Cantidad del producto: "))
        except ValueError:
            raise ValueError(
                "La cantidad debe ser un número entero válido"
            )

        self.agregar_producto(nombre, precio, cantidad)

        print(
            f"\nEl producto '{nombre}' se agregó correctamente."
        )

    def _opcion_vender_producto(self):
        """Solicita los datos necesarios para vender un producto."""
        print("\n--- Vender producto ---")

        nombre = input("Nombre del producto: ").strip()

        if not nombre:
            raise ValueError(
                "El nombre del producto no puede estar vacío"
            )

        try:
            cantidad = int(input("Cantidad que se venderá: "))
        except ValueError:
            raise ValueError(
                "La cantidad debe ser un número entero válido"
            )

        self.vender_producto(nombre, cantidad)

        print(
            f"\nVenta realizada correctamente: "
            f"{cantidad} unidad(es) de '{nombre}'."
        )

    def _opcion_producto_mas_caro(self):
        """Muestra el producto con el precio más alto."""
        resultado = self.producto_mas_caro()

        if resultado is None:
            print("\nEl inventario está vacío.")
        else:
            nombre, precio = resultado

            print("\n--- Producto más caro ---")
            print(f"Nombre: {nombre}")
            print(f"Precio: ${precio:.2f}")

    def _opcion_mostrar_estadisticas(self):
        """Muestra las estadísticas generales del inventario."""
        print("\n--- Estadísticas del inventario ---")
        print(f"Total de productos: {self.total_productos}")
        print(
            f"Valor total del inventario: "
            f"${self.valor_total_inventario:.2f}"
        )

    def _opcion_productos_bajo_stock(self):
        """Muestra los productos cuya cantidad es menor o igual a 5."""
        productos = self.productos_bajo_stock

        if not productos:
            print("\nNo hay productos con bajo stock.")
            return

        print("\n--- Productos con bajo stock ---")
        print(f"{'Producto':<25}{'Precio':>15}{'Cantidad':>15}")
        print("-" * 55)

        for producto in productos:
            print(
                f"{producto['nombre']:<25}"
                f"${producto['precio']:>14.2f}"
                f"{producto['cantidad']:>15}"
            )


# ======================================================
# PROGRAMA PRINCIPAL
# ======================================================


if __name__ == "__main__":
    tienda = InventarioTienda("Mi Tienda")
    tienda.ejecutar()