// app.js
import express from "express";
import session from "express-session";
import path from "path";
import { fileURLToPath } from "url";

// Controladores
import alumnoController from "./controllers/alumnoController.js";
import tareaController from "./controllers/tareaController.js";
import eventoController from "./controllers/eventoController.js";
import notaController from "./controllers/notaController.js";
import recordatorioController from "./controllers/recordatorioController.js";

const app = express();

// Configuración de rutas absolutas
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuración de Express
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Archivos estáticos (CSS, imágenes, JS frontend)
app.use(express.static(path.join(__dirname, "public")));

// Sesiones (si usas login)
app.use(
  session({
    secret: "secreto_super_seguro",
    resave: false,
    saveUninitialized: true,
  })
);

// Motor de plantillas EJS
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

// =========================
//      RUTAS PRINCIPALES
// =========================

// Página principal
app.get("/", (req, res) => {
  res.redirect("/alumnos");
});

// -----------------------------
//        ALUMNOS
// -----------------------------
app.get("/alumnos", alumnoController.listarAlumnos);
app.get("/alumnos/nuevo", alumnoController.formNuevoAlumno);
app.post("/alumnos", alumnoController.crearAlumno);
app.get("/alumnos/:id/editar", alumnoController.formEditarAlumno);
app.put("/alumnos/:id", alumnoController.actualizarAlumno);
app.delete("/alumnos/:id", alumnoController.eliminarAlumno);

// -----------------------------
//        TAREAS
// -----------------------------
app.get("/tareas", tareaController.listarTodas);
app.get("/alumnos/:id/tareas", tareaController.listarPorAlumno);
app.post("/tareas", tareaController.crearTareaMulti);
app.put("/tareas/:id", tareaController.actualizarTarea);
app.delete("/tareas/:id", tareaController.eliminarTarea);

// -----------------------------
//        NOTAS
// -----------------------------
app.get("/notas", notaController.listarNotas);
app.post("/notas", notaController.crearOActualizarNota);
app.delete("/notas/:id", notaController.eliminarNota);

// -----------------------------
//        RECORDATORIOS
// -----------------------------
app.get("/recordatorios", recordatorioController.listarRecordatorios);
app.post("/recordatorios", recordatorioController.crearRecordatorioMulti);
app.put("/recordatorios/:id", recordatorioController.actualizarRecordatorio);
app.delete("/recordatorios/:id", recordatorioController.eliminarRecordatorio);

// -----------------------------
//        EVENTOS
// -----------------------------
app.get("/eventos", eventoController.listarEventos);
app.post("/eventos", eventoController.crearEventoMulti);
app.put("/eventos/:id", eventoController.actualizarEvento);
app.delete("/eventos/:id", eventoController.eliminarEvento);

// -----------------------------
//        PUERTO
// -----------------------------
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});