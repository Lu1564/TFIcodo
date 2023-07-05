console.log(location.search); // Imprime en la consola los argumentos pasados a este formulario
var id = location.pathname.split("/").pop();
console.log(id);
const { createApp } = Vue;
createApp({
    data() {
        return {
            // Inicializa las variables
            id: 0,
            nombre: "",
            imagen: "",
            stock: 0,
            precio: 0,
            id_fabricante:"",
            // url: "http://localhost:5000/prueba/producto/" + id,
            url: "https://luis373.pythonanywhere.com/prueba/producto" + id,
        };
    },
    methods: {
        fetchData(url) {
            fetch(url)
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);
                    this.id = data.id;
                    this.nombre = data.nombre;
                    this.imagen = data.imagen;
                    this.stock = data.stock;
                    this.precio = data.precio;
                    this.id_fabricante = data.id_fabricante
                })
                .catch((err) => {
                    console.error(err);
                    this.error = true;
                });
        },
        modificar() {
            let producto = {
                nombre: this.nombre,
                precio: this.precio,
                stock: this.stock,
                imagen: this.imagen,
                id_fabricante: this.id_fabricante,
            };
            var options = {
                body: JSON.stringify(producto),
                method: "PUT",
                headers: { "Content-Type": "application/json"},
                redirect: "follow",
            };
            fetch(this.url, options)
                .then(function () {
                    alert("Registro actualizado!");
                    //window.location.href = "http://localhost:5000/producto";
                    window.location.href = "https://luis373.pythonanywhere.com/producto";
                })
                .catch((err) => {
                    console.error(err);
                    alert("Error al actualizar.");
                });
        },
    },
    created() {
        this.fetchData(this.url);
    },
}).mount("#app");