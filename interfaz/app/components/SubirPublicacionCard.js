import styles from "./SubirPublicacionCard.module.css";
import {
  DialogBody,
  DialogFooter,
} from "@/components/ui/dialog";
import { FileUploadRoot, FileUploadTrigger } from "@/components/ui/file-upload";
import { FaFile } from "react-icons/fa";
import { MdDelete } from "react-icons/md";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { MdFileUpload } from "react-icons/md";
import { toaster } from "@/components/ui/toaster"

export default function SubirPublicacionCard(props) {
  const { id_list, tipos, setOpen, color, fetchPublicaciones } = props;
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [selectedType, setSelectedType] = useState("");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

// Función para manejar cuando se añaden archivos   
  const handleFileChange = (e) => {
    for (const i of selectedFiles) {
      if (i.name == e.acceptedFiles[0].name) {
        toaster.create({
          title: "El archivo ya fue añadido anteriormente",
          type: "error",
        });
        return;
      }
    }
    setSelectedFiles((prevFiles) => [...prevFiles, e.acceptedFiles[0]]);
  };

//   Función para manejar cuando se elimina un archivo
  const borrarElemento = (index) => {
    const nuevaLista = selectedFiles.filter((_, i) => i !== index);
    setSelectedFiles(nuevaLista);
  };

//   Función para limpiar el formulario
  const clearForm = () => {
    setSelectedFiles([]);
    setSelectedType("");
    setTitle("");
    setDescription("");
  };

//   Función para manejar el envío de la publicación
  const handlePublish = async () => {
    if (
      title == "" ||
      description == "" ||
      selectedFiles.length == 0 ||
      selectedType == "" ||
      selectedType == "Seleccione un tipo"
    ) {
      toaster.create({
        title: "Información Incompleta",
        type: "error",
        duration: 3000,
      });
      return;
    }
    const formData = new FormData();
    selectedFiles.forEach((file) => {
      formData.append("file", file);
    });
    formData.append("title", title);
    formData.append("user", 1);
    formData.append("description", description);
    formData.append("type", selectedType);
    formData.append("asignatura", id_list[1]);

    toaster.create({
      title: "Subiendo Publicación",
      type: "info",
      duration: 5000,
    });
    const response = await fetch("http://172.233.25.94:5000/publicacion", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    console.log(response);
    if (response.status == 200) {
      setOpen(false);
      toaster.create({
        title: "Publicación creada correctamente",
        type: "success",
        duration: 3000,
      });
      fetchPublicaciones();
      clearForm();
    } else {
      toaster.create({
        title: "Publicación no se ha creado correctamente",
        type: "error",
        duration: 3000,
      });
    }
  };

  return (
    <>
      <DialogBody
        className={styles.modalBody}
        display={"flex"}
        flexDirection={"row"}
      >
        <div>
          <p>Titulo de la publicación</p>
          <input
            placeholder="Título"
            className={styles.modalInput}
            onChange={(e) => setTitle(e.target.value)}
            value={title}
          />
          <p>Descripción de la publicacion</p>
          <textarea
            rows={8}
            cols={37}
            className={styles.modalTextArea}
            placeholder="Descripción"
            onChange={(e) => setDescription(e.target.value)}
            value={description}
          />
          <p>Tipo de la publicación</p>
          <select
            id="selectTypes"
            className={styles.modalSelect}
            defaultValue={""}
            onChange={(e) => setSelectedType(e.target.value)}
          >
            <option value="" disabled hidden>
              Seleccione un tipo
            </option>
            {tipos.map((x, index) => (
              <option value={x.id} key={index}>
                {x.nombre}
              </option>
            ))}
          </select>
        </div>
        <div className={styles.divArchivos}>
          <p>Archivos Seleccionados</p>
          <div
            className={styles.divArchivosList}
            style={{
              overflowY: selectedFiles.length > 6 ? "scroll" : "hidden",
            }}
          >
            {selectedFiles.map((file, index) => (
              <div className={styles.divFile} key={index}>
                <FaFile />
                <p className={styles.divFileName}>{file.name}</p>
                <MdDelete
                  size={"1.3rem"}
                  color="red"
                  className={styles.deleteButton}
                  onClick={() => borrarElemento(index)}
                />
              </div>
            ))}
          </div>
          <FileUploadRoot
            marginTop={"1rem"}
            marginLeft={"3.8rem"}
            onFileChange={handleFileChange}
          >
            <FileUploadTrigger>
              <Button as={"div"} className={styles.addFileButton}>
                <MdFileUpload /> Agregar Archivo
              </Button>
            </FileUploadTrigger>
          </FileUploadRoot>
        </div>
      </DialogBody>
      <DialogFooter marginRight={"14.7vw"}>
        <Button
          backgroundColor={color}
          rounded={"full"}
          paddingRight={"4rem"}
          paddingLeft={"4rem"}
          className={styles.publishButton}
          onClick={handlePublish}
        >
          Publicar
        </Button>
      </DialogFooter>
    </>
  );
}
