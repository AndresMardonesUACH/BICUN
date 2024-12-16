"use client";
import { useParams } from "next/navigation";
import styles from "./page.module.css";
import AsignaturaCard from "@/app/components/AsignaturaCard";
import {
  BreadcrumbCurrentLink,
  BreadcrumbLink,
  BreadcrumbRoot,
} from "@/components/ui/breadcrumb";
import Link from "next/link";
import { useState, useEffect } from "react";
import {
  ProgressCircleRing,
  ProgressCircleRoot,
} from "@/components/ui/progress-circle";


function Carrera() {
  const [asignaturasList, setAsignaturasList] = useState([]);
  const { id } = useParams();

  const fetchAsignaturas = async () => {
    const response = await fetch(`http://localhost:5000/asignaturas/${id}`);
    const data = await response.json();
    setAsignaturasList(data);
  };

  useEffect(() => {
    fetchAsignaturas();
  }, []);

  return (
    <div>
      <header className={styles.header}>
        <p className={styles.mainTitle}>BICUN</p>
        <p className={styles.subTitle}>Asignaturas</p>
        <p className={styles.user}>Usuario</p>
      </header>

      <main className={styles.main}>
        <BreadcrumbRoot marginLeft={"2rem"} marginBottom={"1rem"}>
          <BreadcrumbLink href="/" color={"black"}>
            Carreras
          </BreadcrumbLink>
          <BreadcrumbCurrentLink color={"gray"}>
            Asignaturas
          </BreadcrumbCurrentLink>
        </BreadcrumbRoot>
        {asignaturasList.length > 0 ? (
          <>
            <p className={styles.carreraTitle}>{asignaturasList[0].nombre}</p>
            <div className={styles.divAsignaturas}>
              {asignaturasList[0].asignaturas.map((asignatura, index) => (
                <div style={{ marginBottom: "2rem" }} key={index}>
                  <Link href={`/asignatura/${id}-${asignatura.id}`}>
                    <AsignaturaCard
                      nombre={asignatura.nombre}
                      prefijo={asignatura.prefijo}
                      codigo={asignatura.codigo}
                      color={asignatura.color_1}
                    />
                  </Link>
                </div>
              ))}
            </div>
          </>
        ) : (
          <ProgressCircleRoot value={null} size="lg" margin={"auto"} >
            <ProgressCircleRing cap="round" />
          </ProgressCircleRoot>
        )}
      </main>
      
    </div>
  );
}

export default Carrera;
