"use client";
import { useParams } from "next/navigation";
import styles from "./page.module.css";
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"
import { MdFileUpload } from "react-icons/md";
import {BreadcrumbCurrentLink, BreadcrumbLink, BreadcrumbRoot} from "@/components/ui/breadcrumb";
import { useState, useEffect, use } from "react";
import PublicacionCard from "@/app/components/PublicacionCard";


function buscaInfo(data, id) {
  for (const i of data) {
    if (i.id == id) {
      return i;
    }
  }
}

function Asignatura() {
  const { id } = useParams();
  const [publicacionesList, setPublicacionesList] = useState([]);
  const asignaturas = [
        {
          id:1,
          nombre: "Programación",
          prefijo: "INFO",
          codigo: "188",
          color: "#68b0ab",
          publicaciones: [{nombre: "Prueba1", descripcion: "Lorem ipsum", fecha: "2020-10-10", publicador: "rosendo", archivos:[{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"}]}, {nombre: "Prueba2", descripcion: "Lorem ipsum", fecha: "2020-10-10", publicador: "rosendo", archivos:[{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"},{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"},{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"}]}, {nombre: "Prueba3", descripcion: "Lorem ipsum", fecha: "2020-10-10", publicador: "rosendo", archivos:[{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"}]}],
        },
        {
          id:2,
          nombre: "Arquitectura de Software",
          prefijo: "INFO",
          codigo: "189",
          color: "#ff914d",
          publicaciones: [{nombre: "Prueba1", descripcion: "Lorem ipsum", fecha: "2020-10-10", publicador: "rosendo", archivos:[{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"}]}, {nombre: "Prueba2", descripcion: "Lorem ipsum", fecha: "2020-10-10", publicador: "rosendo", archivos:[{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"},{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"},{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"}]}, {nombre: "Prueba3", descripcion: "Lorem ipsum", fecha: "2020-10-10", publicador: "rosendo", archivos:[{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"}]}],
        },
        {
          id:3,
          nombre: "Diseño y Análisis de Algoritmos",
          prefijo: "INFO",
          codigo: "250",
          color: "#924a1e",
          publicaciones: [{nombre: "Prueba1", descripcion: "Lorem ipsum", fecha: "2020-10-10", publicador: "rosendo", archivos:[{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"}]}, {nombre: "Prueba2", descripcion: "Lorem ipsum", fecha: "2020-10-10", publicador: "rosendo", archivos:[{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"},{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"},{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"}]}, {nombre: "Prueba3", descripcion: "Lorem ipsum", fecha: "2020-10-10", publicador: "rosendo", archivos:[{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"}]}],
        },
        {
          id:4,
          nombre: "Bases de Datos",
          prefijo: "INFO",
          codigo: "231",
          color: "#8c52ff",
          publicaciones: [{nombre: "Prueba1", descripcion: "Lorem ipsum", fecha: "2020-10-10", publicador: "rosendo", archivos:[{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"}]}, {nombre: "Prueba2", descripcion: "Lorem ipsum", fecha: "2020-10-10", publicador: "rosendo", archivos:[{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"},{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"},{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"}]}, {nombre: "Prueba3", descripcion: "Lorem ipsum", fecha: "2020-10-10", publicador: "rosendo", archivos:[{nombre: "Archivo1.pdf"}, {nombre: "Archivo2.txt"}]}],
        },
        {
          id:5,
          nombre: "Geometría para Ingeniería",
          prefijo: "BAIN",
          codigo: "067",
          color: "#68b0ab",
        },
        {
          id:6,
          nombre: "Cálculo en Varias Variables",
          prefijo: "BAIN",
          codigo: "094",
          color: "#ff914d",
        },
  ];

  const id_list = id.split("-")

  const fetchPublicaciones = async () => {
    const response = await fetch(`http://localhost:5000/publicaciones/${id_list[1]}`);
    const data = await response.json();
    setPublicacionesList(data);
  };

  useEffect(() => {  
    fetchPublicaciones();
  }, []);

  const tiposPublicaciones = ["Examen", "Guia", "Libro", "Otro"];
  const infoAsignatura = buscaInfo(asignaturas, id_list[1]);
  return (
    <div style={{backgroundColor: "white", color: "black"}}>

      <header className={styles.header} style={{backgroundColor: infoAsignatura.color}}>
        <p className={styles.mainTitle}>BICUN</p>
        <p className={styles.subTitle}>{infoAsignatura.nombre}</p>
        <p className={styles.user}>Usuario</p>
      </header>

      <BreadcrumbRoot marginLeft={"2rem"}  marginTop={"2vh"}>
          <BreadcrumbLink href="/carreras" color={"black"}>Carreras</BreadcrumbLink>
          <BreadcrumbLink href={`/carreras/carrera/${id_list[0]}`} color={"black"}>Asignaturas</BreadcrumbLink>
          <BreadcrumbCurrentLink color={"gray"}>{infoAsignatura.nombre}</BreadcrumbCurrentLink>
        </BreadcrumbRoot>

      <main className={styles.main} style={{backgroundColor: "white", color: "black"}}>

        <div className={styles.divEtiquetas} style={{backgroundColor: infoAsignatura.color}}>
          <p className={styles.divEtiquetasTitle}>Etiquetas</p>
          {tiposPublicaciones.map((x, index) => (
              <Checkbox colorPalette={"gray"} variant={"subtle"} margin={"1vw"} key={index}>{x}</Checkbox>
            ))}
        </div>

        <Button className={styles.divPublicacionesButton} backgroundColor={infoAsignatura.color}><MdFileUpload />Subir Publicación</Button>
        <div className={styles.divPublicaciones}>


            {infoAsignatura.publicaciones.map((x, index) => (
              <PublicacionCard x={x} key={index} color = {infoAsignatura.color}/>
              ))}
        </div>

      </main>
    </div>
  );
}

export default Asignatura;
