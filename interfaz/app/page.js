"use client";
import styles from "./page.module.css";
import { Input } from "@chakra-ui/react";
import { InputGroup } from "@/components/ui/input-group";
import { LuSearch } from "react-icons/lu";
import { IoMdAddCircle } from "react-icons/io";
import AsignaturaCard from "@/app/components/AsignaturaCard";
import "./globals.css";
import Link from "next/link";
import { useState, useEffect } from "react";
import {
  ProgressCircleRing,
  ProgressCircleRoot,
} from "@/components/ui/progress-circle";

function HomeCarreras() {
  const [carreras, setCarreras] = useState([]);

  const fetchCarreras = async () => {
    const response = await fetch("http://172.233.25.94:5000/carreras");
    const data = await response.json();
    setCarreras(data);
  };

  useEffect(() => {
    fetchCarreras();
  }, []);

  return (
    <div>
      <header className={styles.header}>
        <p className={styles.mainTitle}>BICUN</p>
        <p className={styles.subTitle}>Carreras</p>
        <InputGroup
          startElement={<LuSearch color="black" />}
          className={styles.searchBar}
        >
          <Input
            placeholder="Buscar carrera"
            colorScheme={"red"}
            rounded={"full"}
            _placeholder={{ color: "#c8d5b9", fontWeight: "bold" }}
          />
        </InputGroup>
        <p className={styles.user}>Usuario</p>
      </header>

      <main className={styles.main}>
        {carreras.length > 0 ? (
          carreras.map((carrera, index) => (
            <div className={styles.divCarrera} key={index}>
              <Link href={`/carrera/${carrera.id}`}>
                <p className={styles.carreraTitle}>{carrera.nombre}</p>
              </Link>

              <div className={styles.divAsignaturas}>
                {carrera.asignaturas.map((asignatura, index) => (
                  <Link
                    key={index}
                    href={`/asignatura/${carrera.id}-${asignatura.id}`}
                  >
                    <AsignaturaCard
                      nombre={asignatura.nombre}
                      prefijo={asignatura.prefijo}
                      codigo={asignatura.codigo}
                      color={asignatura.color_1}
                    />
                  </Link>
                ))}
                <Link href={`/carrera/${carrera.id}`}>
                  <IoMdAddCircle className={styles.addButton} />
                </Link>
              </div>
            </div>
          ))
        ) : (
          <ProgressCircleRoot value={null} size="lg" margin={"auto"} >
            <ProgressCircleRing cap="round"/>
          </ProgressCircleRoot>
        )}
      </main>
    </div>
  );
}

export default HomeCarreras;
