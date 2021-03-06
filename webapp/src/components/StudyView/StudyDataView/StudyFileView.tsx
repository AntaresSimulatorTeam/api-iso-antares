/* eslint-disable react-hooks/exhaustive-deps */
import React, { useEffect, useState } from 'react';
import { Theme, createStyles, makeStyles } from '@material-ui/core';
import { useSnackbar } from 'notistack';
import { Translation } from 'react-i18next';
import { getFileData } from '../../../services/api/file';
import MainContentLoader from '../../ui/loaders/MainContentLoader';

const useStyles = makeStyles((theme: Theme) => createStyles({
  code: {
    whiteSpace: 'pre',
  },
}));

interface PropTypes {
  url: string;
}

const StudyDataView = (props: PropTypes) => {
  const { url } = props;
  const classes = useStyles();
  const { enqueueSnackbar } = useSnackbar();
  const [data, setData] = useState<string>();
  const [loaded, setLoaded] = useState(false);

  const loadFileData = async (fileUrl: string) => {
    setData(undefined);
    setLoaded(false);
    try {
      const res = await getFileData(fileUrl);
      setData(res);
    } catch (e) {
      enqueueSnackbar(<Translation>{(t) => t('studymanager:failtoretrievedata')}</Translation>, { variant: 'error' });
    } finally {
      setLoaded(true);
    }
  };

  useEffect(() => {
    loadFileData(url);
  }, [url]);

  return (
    <>
      {data && <code className={classes.code}>{data}</code>}
      {!loaded && (
        <div style={{ width: '100%', height: '100%', position: 'relative' }}>
          <MainContentLoader />
        </div>
      )}
    </>
  );
};

export default StudyDataView;
