
@app.post('/upload/download')
async def upload_download(file: UploadFile, db: Session = Depends(get_session)):
    try:
        content_type, _ = mimetypes.guess_type(file.filename)
        if content_type != 'application/pdf':
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        file_obj = File(
            
            
            name=file.filename,
            file_type='pdf',  
            mime_type='application/pdf'
        )
        db.add(file_obj)
        db.commit()
        db.refresh(file_obj)

       
        data = await file.read()
        new_filename = f"{os.path.splitext(file.filename)[0]}_{time.time()}.pdf"
        save_path = os.path.join(UPLOAD_DIR, new_filename)

        with open(save_path, "wb") as f:
            f.write(data)

        return FileResponse(path=save_path, media_type="application/octet-stream", filename=new_filename)
    finally:
        db.close()


