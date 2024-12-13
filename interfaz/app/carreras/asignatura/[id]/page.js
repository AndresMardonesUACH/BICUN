"use client";
import { useParams } from "next/navigation";
import styles from "./page.module.css";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { MdFileUpload } from "react-icons/md";
import {
  BreadcrumbCurrentLink,
  BreadcrumbLink,
  BreadcrumbRoot,
} from "@/components/ui/breadcrumb";
import { useState, useEffect, use } from "react";
import PublicacionCard from "@/app/components/PublicacionCard";
import {
  ProgressCircleRing,
  ProgressCircleRoot,
} from "@/components/ui/progress-circle";

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

  const id_list = id.split("-");

  const fetchPublicaciones = async () => {
    const response = await fetch(
      `http://localhost:5000/publicaciones/${id_list[1]}`
    );
    const data = await response.json();
    console.log(data);
    setPublicacionesList(data);
  };

  useEffect(() => {
    fetchPublicaciones();
  }, []);

  const tiposPublicaciones = ["Examen", "Guia", "Libro", "Otro"];
  return (
    <div style={{ backgroundColor: "white", color: "black" }}>
      <header
        className={styles.header}
        style={{ backgroundColor: publicacionesList.length > 0 ? publicacionesList[0].color_1 : "#ffffff" }}
      >
        <p className={styles.mainTitle}>BICUN</p>
        <p className={styles.subTitle}>{publicacionesList.length > 0 ? publicacionesList[0].nombre: ""}</p>
        <p className={styles.user}>Usuario</p>
      </header>

      <BreadcrumbRoot marginLeft={"2rem"} marginTop={"2vh"}>
        <BreadcrumbLink href="/carreras" color={"black"}>
          Carreras
        </BreadcrumbLink>
        <BreadcrumbLink
          href={`/carreras/carrera/${id_list[0]}`}
          color={"black"}
        >
          Asignaturas
        </BreadcrumbLink>
        <BreadcrumbCurrentLink color={"gray"}>
          {publicacionesList.length > 0 ? publicacionesList[0].nombre: ""}
        </BreadcrumbCurrentLink>
      </BreadcrumbRoot>

      <main
        className={styles.main}
        style={{ backgroundColor: "white", color: "black", minHeight: "100vh" }}
      >
        {publicacionesList.length > 0 ? (
          <>
            <div
              className={styles.divEtiquetas}
              style={{ backgroundColor: publicacionesList[0].color_2 }}
            >
              <p className={styles.divEtiquetasTitle}>Etiquetas</p>
              {tiposPublicaciones.map((x, index) => (
                <Checkbox
                  colorPalette={"gray"}
                  variant={"subtle"}
                  margin={"1vw"}
                  key={index}
                >
                  {x}
                </Checkbox>
              ))}
            </div>

            <Button
              className={styles.divPublicacionesButton}
              backgroundColor={publicacionesList[0].color_1}
            >
              <MdFileUpload />
              Subir Publicación
            </Button>
            <div className={styles.divPublicaciones}>
              {publicacionesList[0].publicaciones.map((x, index) => (
                <PublicacionCard
                  x={x}
                  key={index}
                  color={publicacionesList[0].color_3}
                />
              ))}
            </div>
          </>
        ) : (
          <ProgressCircleRoot value={null} size="lg" margin={"auto"}>
            <ProgressCircleRing cap="round" />
          </ProgressCircleRoot>
        )}
      </main>
    </div>
  );
}

export default Asignatura;
