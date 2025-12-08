
import express from "express";
import session from "express-session";
import path from "path";
import { fileURLToPath } from "url";


import alumnoController from "./controllers/alumnoController.js";
import tareaController from "./controllers/tareaController.js";
import eventoController from "./controllers/eventoController.js";
import notaController from "./controllers/notaController.js";
import recordatorioController from "./controllers/recordatorioController.js";

const app = express();


const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


app.use(express.urlencoded({ extended: true }));
app.use(express.json());


app.use(express.static(path.join(__dirname, "public")));

app.use(
  session({
    secret: "secreto_super_seguro",
    resave: false,
    saveUninitialized: true,
  })
);


app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");


app.get("/api/alumnos", alumnoController.listarAlumnos);
app.post("/api/alumnos", alumnoController.crearAlumno);
app.put("/api/alumnos/:id", alumnoController.actualizarAlumno);
app.delete("/api/alumnos/:id", alumnoController.eliminarAlumno);


app.get("/api/tareas", tareaController.listarTodas);
app.get("/api/alumnos/:id/tareas", tareaController.listarPorAlumno);
app.post("/api/tareas", tareaController.crearTareaMulti);
app.put("/api/tareas/:id", tareaController.actualizarTarea);
app.delete("/api/tareas/:id", tareaController.eliminarTarea);


app.get("/api/notas", notaController.listarNotas);
app.post("/api/notas", notaController.crearOActualizarNota);
app.delete("/api/notas/:id", notaController.eliminarNota);

app.get("/api/recordatorios", recordatorioController.listarRecordatorios);
app.post("/api/recordatorios", recordatorioController.crearRecordatorioMulti);
app.put("/api/recordatorios/:id", recordatorioController.actualizarRecordatorio);
app.delete("/api/recordatorios/:id", recordatorioController.eliminarRecordatorio);


app.get("/api/eventos", eventoController.listarEventos);
app.post("/api/eventos", eventoController.crearEventoMulti);
app.put("/api/eventos/:id", eventoController.actualizarEvento);
app.delete("/api/eventos/:id", eventoController.eliminarEvento);


const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});