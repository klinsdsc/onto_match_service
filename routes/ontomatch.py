import os
import hashlib
import tempfile

from fastapi import APIRouter, HTTPException, File, UploadFile
import pandas as pd
import OntologyMatching

router = APIRouter(tags=["OntologyMatching"], prefix='/OntologyMatching')


@router.post("/ontomatch", include_in_schema=True)
async def ontomatch(ontology: UploadFile = File(...), data: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, mode='wb') as onto_file:
        ontology_content = await ontology.read()
        onto_file.write(ontology_content)
        onto_file_name = onto_file.name

    hash_object = hashlib.sha256()
    hash_object.update(ontology_content)
    hash_hex = hash_object.hexdigest()
    new_onto_file_name = f"/tmp/{hash_hex[:8]}"
    os.rename(onto_file_name, new_onto_file_name)

    with tempfile.NamedTemporaryFile(delete=False, mode='wb') as data_file:
        data_content = await data.read()
        data_file.write(data_content)
        data_file_name = data_file.name

    try:
        df = pd.read_csv(data_file_name)
        if df.empty:
            raise HTTPException(status_code=500, detail="Empty data")

        with tempfile.NamedTemporaryFile(delete=True, mode='w+', encoding='utf-8') as output_file:
            output_file_name = output_file.name
            OntologyMatching.match(new_onto_file_name, data_file_name, output_file_name, 100, 25)
            output_content = output_file.read()
            os.remove(new_onto_file_name)
            os.remove(data_file_name)
            return output_content

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
